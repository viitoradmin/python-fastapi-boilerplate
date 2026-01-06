"""
API Key management service module.

This module contains business logic for API key management operations.
"""
import json
from typing import Optional, List, Tuple

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import constant_variable
from app.models.domain.api_key import ApiKeyDomain
from app.repositories.api_key import ApiKeyRepository
from app.schemas.api_key import ApiKeyUpdateRequest


class ManagementService:
    """
    API Key management service.
    
    Handles business logic for API key CRUD operations and management.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize management service.
        
        Args:
            session: Database session instance
        """
        self.api_key_repository = ApiKeyRepository(session)
    
    async def get_user_api_keys(
        self,
        user_id: int,
        active_only: bool = False,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[ApiKeyDomain], int, bool]:
        """
        Get API keys for a user with pagination.
        
        Args:
            user_id: User ID
            active_only: Whether to return only active keys
            page: Page number (1-based)
            per_page: Items per page
            
        Returns:
            Tuple[List[ApiKeyDomain], int, bool]: (api_keys, total, has_next)
        """
        offset = (page - 1) * per_page
        api_keys, total = await self.api_key_repository.get_user_api_keys(
            user_id=user_id,
            active_only=active_only,
            limit=per_page,
            offset=offset
        )
        
        has_next = offset + len(api_keys) < total
        
        return [ApiKeyDomain.from_orm(key) for key in api_keys], total, has_next
    
    async def get_api_key(self, api_key_id: int, user_id: int) -> Optional[ApiKeyDomain]:
        """
        Get a specific API key for a user.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            Optional[ApiKeyDomain]: API key domain if found and owned by user
        """
        api_key = await self.api_key_repository.get_by_id(api_key_id)
        
        if api_key and api_key.user_id == user_id:
            return ApiKeyDomain.from_orm(api_key)
        
        return None
    
    async def update_api_key(
        self,
        api_key_id: int,
        user_id: int,
        update_data: ApiKeyUpdateRequest
    ) -> Optional[ApiKeyDomain]:
        """
        Update an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            update_data: Update data
            
        Returns:
            Optional[ApiKeyDomain]: Updated API key domain
            
        Raises:
            HTTPException: If duplicate name or validation errors
        """
        # Check for duplicate name if name is being updated
        if update_data.name:
            existing_keys, _ = await self.api_key_repository.get_user_api_keys(user_id)
            if any(key.name == update_data.name and key.id != api_key_id for key in existing_keys):
                raise HTTPException(
                    status_code=constant_variable.HTTP_409_CONFLICT,
                    detail=constant_variable.API_KEY_MESSAGES["DUPLICATE_NAME"]
                )
        
        # Prepare update data
        update_dict = {}
        
        if update_data.name is not None:
            update_dict["name"] = update_data.name
        
        if update_data.is_active is not None:
            update_dict["is_active"] = update_data.is_active
        
        if update_data.scopes is not None:
            update_dict["scopes"] = json.dumps(update_data.scopes)
        
        if update_data.allowed_ips is not None:
            update_dict["allowed_ips"] = json.dumps(update_data.allowed_ips)
        
        if update_data.rate_limit is not None:
            update_dict["rate_limit"] = update_data.rate_limit
        
        if update_data.expires_at is not None:
            update_dict["expires_at"] = update_data.expires_at
        
        # Update API key
        updated_key = await self.api_key_repository.update_api_key(
            api_key_id=api_key_id,
            user_id=user_id,
            **update_dict
        )
        
        return ApiKeyDomain.from_orm(updated_key) if updated_key else None
    
    async def delete_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Delete an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            bool: True if deleted successfully
        """
        return await self.api_key_repository.delete_api_key(api_key_id, user_id)
    
    async def revoke_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Revoke (deactivate) an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            bool: True if revoked successfully
        """
        return await self.api_key_repository.deactivate_api_key(api_key_id, user_id)
    
    async def search_api_keys(
        self,
        user_id: int,
        search_term: Optional[str] = None,
        is_active: Optional[bool] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[ApiKeyDomain], int, bool]:
        """
        Search API keys with filters.
        
        Args:
            user_id: User ID
            search_term: Search term
            is_active: Filter by active status
            page: Page number
            per_page: Items per page
            
        Returns:
            Tuple[List[ApiKeyDomain], int, bool]: (api_keys, total, has_next)
        """
        offset = (page - 1) * per_page
        api_keys, total = await self.api_key_repository.search_api_keys(
            user_id=user_id,
            search_term=search_term,
            is_active=is_active,
            limit=per_page,
            offset=offset
        )
        
        has_next = offset + len(api_keys) < total
        
        return [ApiKeyDomain.from_orm(key) for key in api_keys], total, has_next
    
    async def cleanup_expired_keys(self) -> int:
        """
        Clean up expired API keys.
        
        Returns:
            int: Number of keys cleaned up
        """
        return await self.api_key_repository.cleanup_expired_keys()