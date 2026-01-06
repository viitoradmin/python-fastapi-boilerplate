"""
Main API Key service module.

This module provides a unified interface for all API key operations.
"""
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.api_key import ApiKeyDomain
from app.schemas.api_key import (
    ApiKeyCreateRequest,
    ApiKeyUpdateRequest,
    ApiKeyValidationResponse
)
from app.services.api_key.creation_service import CreationService
from app.services.api_key.validation_service import ValidationService
from app.services.api_key.management_service import ManagementService
from app.services.api_key.usage_service import UsageService


class ApiKeyService:
    """
    Main API Key service.
    
    Provides a unified interface for API key operations by delegating
    to specialized services.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize API key service.
        
        Args:
            session: Database session instance
        """
        self.creation_service = CreationService(session)
        self.validation_service = ValidationService(session)
        self.management_service = ManagementService(session)
        self.usage_service = UsageService(session)
    
    async def create_api_key(
        self,
        user_id: int,
        create_data: ApiKeyCreateRequest
    ) -> Tuple[ApiKeyDomain, str]:
        """
        Create a new API key for a user.
        
        Args:
            user_id: User ID
            create_data: API key creation data
            
        Returns:
            Tuple[ApiKeyDomain, str]: (api_key_domain, actual_api_key)
            
        Raises:
            HTTPException: If user not found or max keys reached
        """
        return await self.creation_service.create_api_key(user_id, create_data)
    
    async def validate_api_key(
        self,
        api_key: str,
        required_scope: Optional[str] = None,
        client_ip: Optional[str] = None
    ) -> ApiKeyValidationResponse:
        """
        Validate an API key and check permissions.
        
        Args:
            api_key: The API key to validate
            required_scope: Required scope for the operation
            client_ip: Client IP address
            
        Returns:
            ApiKeyValidationResponse: Validation result
        """
        return await self.validation_service.validate_api_key(api_key, required_scope, client_ip)
    
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
        return await self.management_service.get_user_api_keys(user_id, active_only, page, per_page)
    
    async def get_api_key(self, api_key_id: int, user_id: int) -> Optional[ApiKeyDomain]:
        """
        Get a specific API key for a user.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            Optional[ApiKeyDomain]: API key domain if found and owned by user
        """
        return await self.management_service.get_api_key(api_key_id, user_id)
    
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
        return await self.management_service.update_api_key(api_key_id, user_id, update_data)
    
    async def delete_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Delete an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            bool: True if deleted successfully
        """
        return await self.management_service.delete_api_key(api_key_id, user_id)
    
    async def revoke_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Revoke (deactivate) an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            bool: True if revoked successfully
        """
        return await self.management_service.revoke_api_key(api_key_id, user_id)
    
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
        return await self.management_service.search_api_keys(user_id, search_term, is_active, page, per_page)
    
    async def cleanup_expired_keys(self) -> int:
        """
        Clean up expired API keys.
        
        Returns:
            int: Number of keys cleaned up
        """
        return await self.management_service.cleanup_expired_keys()
    
    async def get_api_key_usage_stats(self, api_key_id: int, user_id: int) -> Optional[dict]:
        """
        Get usage statistics for an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            Optional[dict]: Usage statistics if key found and owned by user
        """
        return await self.usage_service.get_api_key_usage_stats(api_key_id, user_id)