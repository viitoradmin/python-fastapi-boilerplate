"""
API Key validation service module.

This module contains business logic for API key validation operations.
"""
from typing import Optional

from app.core.utils import constant_variable
from app.models.domain.api_key import ApiKeyDomain
from app.repositories.api_key import ApiKeyRepository
from app.schemas.api_key import ApiKeyValidationResponse
from app.utils.api_key import (
    verify_api_key,
    is_valid_api_key_format,
    extract_key_prefix
)
from sqlalchemy.ext.asyncio import AsyncSession


class ValidationService:
    """
    API Key validation service.
    
    Handles business logic for API key validation and permission checking.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize validation service.
        
        Args:
            session: Database session instance
        """
        self.api_key_repository = ApiKeyRepository(session)
    
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
        # Check format
        if not is_valid_api_key_format(api_key):
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["INVALID_FORMAT"]
            )
        
        # Extract prefix and find key
        key_prefix = extract_key_prefix(api_key)
        stored_key = await self.api_key_repository.get_by_prefix(key_prefix)
        
        if not stored_key:
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["INVALID_KEY"]
            )
        
        # Verify the key hash
        if not verify_api_key(api_key, stored_key.key_hash):
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["INVALID_KEY"]
            )
        
        # Check if key is active
        if not stored_key.is_active:
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["INACTIVE_KEY"]
            )
        
        # Check if key is expired
        if stored_key.is_expired:
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["EXPIRED_KEY"]
            )
        
        # Convert to domain model for business logic
        key_domain = ApiKeyDomain.from_orm(stored_key)
        
        # Check scope permissions
        if required_scope and not key_domain.has_scope(required_scope):
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["INSUFFICIENT_SCOPE"]
            )
        
        # Check IP restrictions
        if client_ip and not key_domain.is_ip_allowed(client_ip):
            return ApiKeyValidationResponse(
                is_valid=False,
                error_message=constant_variable.API_KEY_MESSAGES["IP_NOT_ALLOWED"]
            )
        
        # Update usage statistics
        await self.api_key_repository.update_usage(stored_key.id)
        
        # Return successful validation
        return ApiKeyValidationResponse(
            is_valid=True,
            api_key_id=stored_key.id,
            user_id=stored_key.user_id,
            scopes=key_domain.scopes,
            rate_limit=stored_key.rate_limit,
            remaining_requests=stored_key.rate_limit - 1  # Simplified, would need Redis for real rate limiting
        )