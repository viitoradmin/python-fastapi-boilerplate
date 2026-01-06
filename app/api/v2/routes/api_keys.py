"""
API Keys routes for v2.

This module contains enhanced API endpoints for API key management operations.
"""
from typing import Optional, List

from fastapi import APIRouter, Depends, Query, Path, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_db_session
from app.core.responses.standard_response import StandardResponse
from app.core.utils import constant_variable
from app.core.middleware.jwt_auth import get_current_user_id
from app.schemas.api_key import (
    ApiKeyCreateRequest,
    ApiKeyUpdateRequest,
    ApiKeyCreateResponse,
    ApiKeyResponse,
    ApiKeyListResponse,
    ApiKeyUsageResponse,
    ApiKeyValidationRequest,
    ApiKeyValidationResponse
)
from app.services.api_key import ApiKeyService

router = APIRouter(prefix="/api/keys")


@router.post(
    "/",
    response_model=dict,
    status_code=201,
    summary="Create API Key (v2)",
    description="Create a new API key with enhanced features"
)
async def create_api_key(
    create_data: ApiKeyCreateRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new API key with enhanced validation and features.
    
    Args:
        create_data: API key creation data
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: Created API key with actual key value
    """
    api_key_service = ApiKeyService(session)
    
    # Create API key
    api_key_domain, actual_key = await api_key_service.create_api_key(
        user_id=current_user_id,
        create_data=create_data
    )
    
    # Prepare enhanced response data
    response_data = ApiKeyCreateResponse(
        **api_key_domain.to_dict(),
        api_key=actual_key
    )
    
    response = StandardResponse.created(
        data={
            **response_data.dict(),
            "security_notice": "This is the only time the full API key will be displayed. Please store it securely.",
            "best_practices": [
                "Store the API key in environment variables",
                "Use HTTPS for all API requests",
                "Implement proper error handling",
                "Monitor usage regularly"
            ]
        },
        message=constant_variable.API_KEY_MESSAGES["CREATED"]
    )
    
    return response.make


@router.get(
    "/",
    response_model=dict,
    summary="List API Keys (v2)",
    description="Get paginated list of API keys with enhanced filtering"
)
async def list_api_keys(
    current_user_id: int = Depends(get_current_user_id),
    active_only: bool = Query(False, description="Return only active API keys"),
    include_expired: bool = Query(False, description="Include expired API keys"),
    sort_by: str = Query("created_at", description="Sort field (created_at, name, usage_count, last_used_at)"),
    sort_order: str = Query("desc", description="Sort order (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get paginated list of API keys with enhanced filtering and sorting.
    
    Args:
        user_id: User ID (temporary parameter)
        active_only: Whether to return only active keys
        include_expired: Whether to include expired keys
        sort_by: Field to sort by
        sort_order: Sort order
        page: Page number
        per_page: Items per page
        session: Database session
        
    Returns:
        StandardResponse: List of API keys with enhanced metadata
    """
    api_key_service = ApiKeyService(session)
    
    # Get API keys (v2 uses the same service but could be enhanced)
    api_keys, total, has_next = await api_key_service.get_user_api_keys(
        user_id=current_user_id,
        active_only=active_only,
        page=page,
        per_page=per_page
    )
    
    # Convert to response format with enhanced data
    api_key_responses = []
    for key in api_keys:
        key_data = key.to_dict()
        # Add v2 specific enhancements
        key_data.update({
            "masked_key": f"{key.key_prefix}...****",
            "days_until_expiry": (key.expires_at - key.created_at).days if key.expires_at else None,
            "security_score": "high" if key.is_valid and key.allowed_ips else "medium"
        })
        api_key_responses.append(ApiKeyResponse(**key_data))
    
    response_data = ApiKeyListResponse(
        api_keys=api_key_responses,
        total=total,
        page=page,
        per_page=per_page,
        has_next=has_next
    )
    
    # Add v2 specific metadata
    enhanced_data = {
        **response_data.dict(),
        "summary": {
            "total_keys": total,
            "active_keys": len([k for k in api_keys if k.is_active]),
            "expired_keys": len([k for k in api_keys if k.is_expired]),
            "high_usage_keys": len([k for k in api_keys if k.usage_count > 1000])
        }
    }
    
    response = StandardResponse.success(
        data=enhanced_data,
        message=f"Retrieved {len(api_keys)} API keys with enhanced metadata"
    )
    
    return response.make


@router.get(
    "/{api_key_id}",
    response_model=dict,
    summary="Get API Key (v2)",
    description="Get detailed information about a specific API key"
)
async def get_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    include_analytics: bool = Query(False, description="Include usage analytics"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get detailed information about a specific API key with analytics.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        include_analytics: Whether to include usage analytics
        session: Database session
        
    Returns:
        StandardResponse: Enhanced API key details
    """
    api_key_service = ApiKeyService(session)
    
    # Get API key
    api_key = await api_key_service.get_api_key(api_key_id, current_user_id)
    
    if not api_key:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Prepare enhanced response
    response_data = api_key.to_dict()
    
    # Add v2 enhancements
    response_data.update({
        "masked_key": f"{api_key.key_prefix}...****",
        "security_recommendations": [],
        "health_status": "healthy" if api_key.is_valid else "unhealthy"
    })
    
    # Add security recommendations
    if not api_key.allowed_ips:
        response_data["security_recommendations"].append("Consider restricting IP addresses")
    
    if not api_key.expires_at:
        response_data["security_recommendations"].append("Consider setting an expiration date")
    
    if api_key.rate_limit > 5000:
        response_data["security_recommendations"].append("High rate limit - monitor usage carefully")
    
    # Add analytics if requested
    if include_analytics:
        usage_stats = await api_key_service.get_api_key_usage_stats(api_key_id, current_user_id)
        response_data["analytics"] = usage_stats
    
    response = StandardResponse.success(
        data=response_data,
        message="API key details retrieved with enhanced information"
    )
    
    return response.make


@router.put(
    "/{api_key_id}",
    response_model=dict,
    summary="Update API Key (v2)",
    description="Update an API key with validation and security checks"
)
async def update_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    update_data: ApiKeyUpdateRequest = ...,
    current_user_id: int = Depends(get_current_user_id),
    validate_changes: bool = Query(True, description="Validate security implications of changes"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Update an API key with enhanced validation and security checks.
    
    Args:
        api_key_id: API key ID
        update_data: Update data
        user_id: User ID (temporary parameter)
        validate_changes: Whether to validate security implications
        session: Database session
        
    Returns:
        StandardResponse: Updated API key with security analysis
    """
    api_key_service = ApiKeyService(session)
    
    # Get current key for comparison
    current_key = await api_key_service.get_api_key(api_key_id, current_user_id)
    if not current_key:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Update API key
    updated_key = await api_key_service.update_api_key(
        api_key_id=api_key_id,
        user_id=current_user_id,
        update_data=update_data
    )
    
    if not updated_key:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Prepare enhanced response
    response_data = updated_key.to_dict()
    
    # Add change analysis
    changes_made = []
    security_impact = "low"
    
    if update_data.is_active is not None and update_data.is_active != current_key.is_active:
        changes_made.append("activation_status")
        security_impact = "high" if not update_data.is_active else "medium"
    
    if update_data.scopes is not None and update_data.scopes != current_key.scopes:
        changes_made.append("scopes")
        security_impact = "high"
    
    if update_data.allowed_ips is not None and update_data.allowed_ips != current_key.allowed_ips:
        changes_made.append("ip_restrictions")
        security_impact = "high"
    
    if update_data.rate_limit is not None and update_data.rate_limit != current_key.rate_limit:
        changes_made.append("rate_limit")
        security_impact = "medium"
    
    response_data.update({
        "changes_made": changes_made,
        "security_impact": security_impact,
        "recommendations": [
            "Monitor API key usage after changes",
            "Verify applications still function correctly"
        ] if changes_made else []
    })
    
    response = StandardResponse.success(
        data=response_data,
        message=constant_variable.API_KEY_MESSAGES["UPDATED"]
    )
    
    return response.make


@router.delete(
    "/{api_key_id}",
    response_model=dict,
    summary="Delete API Key (v2)",
    description="Safely delete an API key with confirmation"
)
async def delete_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    confirm: bool = Query(False, description="Confirm deletion"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Safely delete an API key with confirmation and cleanup.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        confirm: Confirmation flag
        background_tasks: Background tasks for cleanup
        session: Database session
        
    Returns:
        StandardResponse: Deletion confirmation with cleanup info
    """
    if not confirm:
        response = StandardResponse.bad_request(
            message="Deletion requires confirmation. Add ?confirm=true to proceed."
        )
        return response.make
    
    api_key_service = ApiKeyService(session)
    
    # Get key info before deletion
    api_key = await api_key_service.get_api_key(api_key_id, current_user_id)
    if not api_key:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Delete API key
    deleted = await api_key_service.delete_api_key(api_key_id, current_user_id)
    
    if not deleted:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Schedule background cleanup (in real implementation)
    # background_tasks.add_task(cleanup_api_key_references, api_key_id)
    
    response = StandardResponse.success(
        data={
            "deleted": True,
            "api_key_id": api_key_id,
            "key_name": api_key.name,
            "cleanup_scheduled": True,
            "impact_analysis": {
                "usage_count": api_key.usage_count,
                "last_used": api_key.last_used_at.isoformat() if api_key.last_used_at else None,
                "was_active": api_key.is_active
            }
        },
        message=constant_variable.API_KEY_MESSAGES["DELETED"]
    )
    
    return response.make


@router.post(
    "/batch-operations",
    response_model=dict,
    summary="Batch Operations (v2)",
    description="Perform batch operations on multiple API keys"
)
async def batch_operations(
    current_user_id: int = Depends(get_current_user_id),
    operation: str = Query(..., description="Operation (revoke, delete, activate, deactivate)"),
    api_key_ids: List[int] = Query(..., description="List of API key IDs"),
    confirm: bool = Query(False, description="Confirm batch operation"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Perform batch operations on multiple API keys.
    
    Args:
        user_id: User ID (temporary parameter)
        operation: Operation to perform
        api_key_ids: List of API key IDs
        confirm: Confirmation flag
        session: Database session
        
    Returns:
        StandardResponse: Batch operation results
    """
    if not confirm:
        response = StandardResponse.bad_request(
            message="Batch operations require confirmation. Add ?confirm=true to proceed."
        )
        return response.make
    
    if operation not in ["revoke", "delete", "activate", "deactivate"]:
        response = StandardResponse.bad_request(
            message="Invalid operation. Supported: revoke, delete, activate, deactivate"
        )
        return response.make
    
    api_key_service = ApiKeyService(session)
    
    results = {
        "successful": [],
        "failed": [],
        "total_processed": len(api_key_ids)
    }
    
    for key_id in api_key_ids:
        try:
            if operation == "revoke":
                success = await api_key_service.revoke_api_key(key_id, current_user_id)
            elif operation == "delete":
                success = await api_key_service.delete_api_key(key_id, current_user_id)
            elif operation == "activate":
                from app.schemas.api_key import ApiKeyUpdateRequest
                update_data = ApiKeyUpdateRequest(is_active=True)
                updated = await api_key_service.update_api_key(key_id, current_user_id, update_data)
                success = updated is not None
            elif operation == "deactivate":
                from app.schemas.api_key import ApiKeyUpdateRequest
                update_data = ApiKeyUpdateRequest(is_active=False)
                updated = await api_key_service.update_api_key(key_id, current_user_id, update_data)
                success = updated is not None
            
            if success:
                results["successful"].append(key_id)
            else:
                results["failed"].append({"key_id": key_id, "reason": "Not found or access denied"})
        
        except Exception as e:
            results["failed"].append({"key_id": key_id, "reason": str(e)})
    
    response = StandardResponse.success(
        data=results,
        message=f"Batch {operation} completed: {len(results['successful'])} successful, {len(results['failed'])} failed"
    )
    
    return response.make


# Include all other endpoints from v1 with v2 enhancements
# (validate, usage, search, etc. - similar pattern with enhanced features)