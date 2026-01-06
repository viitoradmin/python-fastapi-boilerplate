"""
API Keys routes for v1.

This module contains API endpoints for API key management operations.
"""
from typing import Optional

from fastapi import APIRouter, Depends, Query, Path
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

router = APIRouter(prefix="/api/keys",)


@router.post(
    "/",
    response_model=dict,
    status_code=201,
    summary="Create API Key",
    description="Create a new API key for the authenticated user"
)
async def create_api_key(
    create_data: ApiKeyCreateRequest,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Create a new API key.
    
    Args:
        create_data: API key creation data
        current_user_id: Current user ID from JWT token
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
    
    # Prepare response data with proper datetime serialization
    api_key_dict = api_key_domain.to_dict()
    api_key_dict["api_key"] = actual_key
    
    response = StandardResponse.created(
        data=api_key_dict,
        message=constant_variable.API_KEY_MESSAGES["CREATED"]
    )
    
    return response.make


@router.get(
    "/",
    response_model=dict,
    summary="List API Keys",
    description="Get paginated list of API keys for the authenticated user"
)
async def list_api_keys(
    current_user_id: int = Depends(get_current_user_id),
    active_only: bool = Query(False, description="Return only active API keys"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get paginated list of API keys for a user.
    
    Args:
        current_user_id: Current user ID from JWT token
        active_only: Whether to return only active keys
        page: Page number
        per_page: Items per page
        session: Database session
        
    Returns:
        StandardResponse: List of API keys with pagination info
    """
    api_key_service = ApiKeyService(session)
    
    # Get API keys
    api_keys, total, has_next = await api_key_service.get_user_api_keys(
        user_id=current_user_id,
        active_only=active_only,
        page=page,
        per_page=per_page
    )
    
    # Convert to response format
    # Convert to dict format to avoid datetime serialization issues
    api_key_dicts = [key.to_dict() for key in api_keys]
    
    response_data = {
        "api_keys": api_key_dicts,
        "total": total,
        "page": page,
        "per_page": per_page,
        "has_next": has_next
    }
    
    response = StandardResponse.success(
        data=response_data,
        message=f"Retrieved {len(api_keys)} API keys"
    )
    
    return response.make


@router.get(
    "/{api_key_id}",
    response_model=dict,
    summary="Get API Key",
    description="Get details of a specific API key"
)
async def get_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get details of a specific API key.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: API key details
    """
    api_key_service = ApiKeyService(session)
    
    # Get API key
    api_key = await api_key_service.get_api_key(api_key_id, current_user_id)
    
    if not api_key:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Use dict format to avoid datetime serialization issues
    response = StandardResponse.success(
        data=api_key.to_dict(),
        message="API key retrieved successfully"
    )
    
    return response.make


@router.put(
    "/{api_key_id}",
    response_model=dict,
    summary="Update API Key",
    description="Update an existing API key"
)
async def update_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    update_data: ApiKeyUpdateRequest = ...,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Update an existing API key.
    
    Args:
        api_key_id: API key ID
        update_data: Update data
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: Updated API key details
    """
    api_key_service = ApiKeyService(session)
    
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
    
    # Use dict format to avoid datetime serialization issues
    response = StandardResponse.success(
        data=updated_key.to_dict(),
        message=constant_variable.API_KEY_MESSAGES["UPDATED"]
    )
    
    return response.make


@router.delete(
    "/{api_key_id}",
    response_model=dict,
    summary="Delete API Key",
    description="Delete an API key permanently"
)
async def delete_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Delete an API key permanently.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: Deletion confirmation
    """
    api_key_service = ApiKeyService(session)
    
    # Delete API key
    deleted = await api_key_service.delete_api_key(api_key_id, current_user_id)
    
    if not deleted:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    response = StandardResponse.success(
        data={"deleted": True, "api_key_id": api_key_id},
        message=constant_variable.API_KEY_MESSAGES["DELETED"]
    )
    
    return response.make


@router.post(
    "/{api_key_id}/revoke",
    response_model=dict,
    summary="Revoke API Key",
    description="Revoke (deactivate) an API key"
)
async def revoke_api_key(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Revoke (deactivate) an API key.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: Revocation confirmation
    """
    api_key_service = ApiKeyService(session)
    
    # Revoke API key
    revoked = await api_key_service.revoke_api_key(api_key_id, current_user_id)
    
    if not revoked:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    response = StandardResponse.success(
        data={"revoked": True, "api_key_id": api_key_id},
        message=constant_variable.API_KEY_MESSAGES["REVOKED"]
    )
    
    return response.make


@router.get(
    "/{api_key_id}/usage",
    response_model=dict,
    summary="Get API Key Usage",
    description="Get usage statistics for an API key"
)
async def get_api_key_usage(
    api_key_id: int = Path(..., description="API key ID"),
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Get usage statistics for an API key.
    
    Args:
        api_key_id: API key ID
        user_id: User ID (temporary parameter)
        session: Database session
        
    Returns:
        StandardResponse: Usage statistics
    """
    api_key_service = ApiKeyService(session)
    
    # Get usage stats
    usage_stats = await api_key_service.get_api_key_usage_stats(api_key_id, current_user_id)
    
    if not usage_stats:
        response = StandardResponse.not_found(
            message=constant_variable.API_KEY_MESSAGES["NOT_FOUND"]
        )
        return response.make
    
    # Usage stats already have properly serialized datetime fields
    response = StandardResponse.success(
        data=usage_stats,
        message="Usage statistics retrieved successfully"
    )
    
    return response.make


@router.post(
    "/validate",
    response_model=dict,
    summary="Validate API Key",
    description="Validate an API key and check permissions"
)
async def validate_api_key(
    validation_data: ApiKeyValidationRequest,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Validate an API key and check permissions.
    
    Args:
        validation_data: Validation request data
        session: Database session
        
    Returns:
        StandardResponse: Validation result
    """
    api_key_service = ApiKeyService(session)
    
    # Validate API key
    validation_result = await api_key_service.validate_api_key(
        api_key=validation_data.api_key,
        required_scope=validation_data.scope,
        client_ip=validation_data.ip_address
    )
    
    # Use validation result directly (no datetime fields to worry about)
    validation_data = validation_result.dict()
    
    if validation_result.is_valid:
        response = StandardResponse.success(
            data=validation_data,
            message=constant_variable.API_KEY_MESSAGES["VALIDATION_SUCCESS"]
        )
    else:
        response = StandardResponse.unauthorized(
            data=validation_data,
            message=validation_result.error_message or constant_variable.API_KEY_MESSAGES["INVALID_KEY"]
        )
    
    return response.make


@router.get(
    "/search",
    response_model=dict,
    summary="Search API Keys",
    description="Search API keys with filters"
)
async def search_api_keys(
    current_user_id: int = Depends(get_current_user_id),
    q: Optional[str] = Query(None, description="Search term for name or prefix"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(get_db_session)
):
    """
    Search API keys with filters.
    
    Args:
        user_id: User ID (temporary parameter)
        q: Search term
        active: Filter by active status
        page: Page number
        per_page: Items per page
        session: Database session
        
    Returns:
        StandardResponse: Search results with pagination
    """
    api_key_service = ApiKeyService(session)
    
    # Search API keys
    api_keys, total, has_next = await api_key_service.search_api_keys(
        user_id=current_user_id,
        search_term=q,
        is_active=active,
        page=page,
        per_page=per_page
    )
    
    # Convert to response format
    # Convert to dict format to avoid datetime serialization issues
    api_key_dicts = [key.to_dict() for key in api_keys]
    
    response_data = {
        "api_keys": api_key_dicts,
        "total": total,
        "page": page,
        "per_page": per_page,
        "has_next": has_next
    }
    
    response = StandardResponse.success(
        data=response_data,
        message=f"Found {len(api_keys)} API keys"
    )
    
    return response.make