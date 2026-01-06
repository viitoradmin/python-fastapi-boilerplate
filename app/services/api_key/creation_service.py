"""
API Key creation service module.

This module contains business logic for API key creation operations.
"""
import json
from typing import Tuple
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import constant_variable
from app.models.domain.api_key import ApiKeyDomain
from app.repositories.api_key import ApiKeyRepository
from app.repositories.user import UserRepository
from app.schemas.api_key import ApiKeyCreateRequest
from app.utils.api_key import (
    generate_api_key,
    generate_api_key_with_expiry
)


class CreationService:
    """
    API Key creation service.
    
    Handles business logic for API key creation.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize creation service.
        
        Args:
            session: Database session instance
        """
        self.api_key_repository = ApiKeyRepository(session)
        self.user_repository = UserRepository(session)
    
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
        # Check if user exists
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=constant_variable.HTTP_404_NOT_FOUND,
                detail=constant_variable.AUTH_MESSAGES["USER_NOT_FOUND"]
            )
        
        # Check if user has reached max API keys limit
        current_count = await self.api_key_repository.count_user_api_keys(user_id)
        if current_count >= constant_variable.API_KEY_DEFAULTS["MAX_KEYS_PER_USER"]:
            raise HTTPException(
                status_code=constant_variable.HTTP_400_BAD_REQUEST,
                detail=constant_variable.API_KEY_MESSAGES["MAX_KEYS_REACHED"]
            )
        
        # Check for duplicate name
        existing_keys, _ = await self.api_key_repository.get_user_api_keys(user_id)
        if any(key.name == create_data.name for key in existing_keys):
            raise HTTPException(
                status_code=constant_variable.HTTP_409_CONFLICT,
                detail=constant_variable.API_KEY_MESSAGES["DUPLICATE_NAME"]
            )
        
        # Generate API key
        if create_data.expires_at:
            # Handle timezone-aware datetime comparison
            now = datetime.now(timezone.utc)
            expires_at_aware = create_data.expires_at
            
            # If the expiration datetime is timezone-naive, assume it's UTC
            if expires_at_aware.tzinfo is None:
                expires_at_aware = expires_at_aware.replace(tzinfo=timezone.utc)
            
            days_until_expiry = (expires_at_aware - now).days
            full_key, key_prefix, key_hash, expires_at = generate_api_key_with_expiry(days_until_expiry)
        else:
            full_key, key_prefix, key_hash = generate_api_key()
            expires_at = create_data.expires_at
        
        # Prepare JSON fields
        scopes_json = json.dumps(create_data.scopes) if create_data.scopes else None
        allowed_ips_json = json.dumps(create_data.allowed_ips) if create_data.allowed_ips else None
        
        # Create API key in database
        api_key = await self.api_key_repository.create_api_key(
            name=create_data.name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            user_id=user_id,
            scopes=scopes_json,
            allowed_ips=allowed_ips_json,
            rate_limit=create_data.rate_limit,
            expires_at=expires_at
        )
        
        return ApiKeyDomain.from_orm(api_key), full_key