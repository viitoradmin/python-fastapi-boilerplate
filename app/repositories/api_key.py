"""
API Key repository module.

This module contains the repository class for API key database operations.
"""
from typing import Optional, List, Tuple
from datetime import datetime

from sqlalchemy import select, update, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.api_key import ApiKey
from app.repositories.base import BaseRepository


class ApiKeyRepository(BaseRepository[ApiKey]):
    """
    API Key repository.
    
    Handles database operations for API key entities.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize API key repository.
        
        Args:
            session: Database session instance
        """
        super().__init__(ApiKey, session)
    
    async def create_api_key(
        self,
        name: str,
        key_hash: str,
        key_prefix: str,
        user_id: int,
        scopes: Optional[str] = None,
        allowed_ips: Optional[str] = None,
        rate_limit: int = 1000,
        expires_at: Optional[datetime] = None
    ) -> ApiKey:
        """
        Create a new API key.
        
        Args:
            name: API key name
            key_hash: Hashed API key
            key_prefix: API key prefix for identification
            user_id: Owner user ID
            scopes: JSON string of allowed scopes
            allowed_ips: JSON string of allowed IP addresses
            rate_limit: Requests per hour limit
            expires_at: Expiration date
            
        Returns:
            ApiKey: Created API key instance
        """
        return await self.create(
            name=name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            user_id=user_id,
            scopes=scopes,
            allowed_ips=allowed_ips,
            rate_limit=rate_limit,
            expires_at=expires_at
        )
    
    async def get_by_hash(self, key_hash: str) -> Optional[ApiKey]:
        """
        Get API key by hash.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            Optional[ApiKey]: API key instance if found
        """
        return await self.get_by_field("key_hash", key_hash)
    
    async def get_by_prefix(self, key_prefix: str) -> Optional[ApiKey]:
        """
        Get API key by prefix.
        
        Args:
            key_prefix: API key prefix
            
        Returns:
            Optional[ApiKey]: API key instance if found
        """
        return await self.get_by_field("key_prefix", key_prefix)
    
    async def get_user_api_keys(
        self,
        user_id: int,
        active_only: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ApiKey], int]:
        """
        Get API keys for a user with pagination.
        
        Args:
            user_id: User ID
            active_only: Whether to return only active keys
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Tuple[List[ApiKey], int]: (api_keys, total_count)
        """
        # Build query conditions
        conditions = [ApiKey.user_id == user_id]
        if active_only:
            conditions.append(ApiKey.is_active == True)
        
        # Get total count
        count_query = select(func.count(ApiKey.id)).where(and_(*conditions))
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar()
        
        # Get paginated results
        query = (
            select(ApiKey)
            .where(and_(*conditions))
            .order_by(ApiKey.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(query)
        api_keys = result.scalars().all()
        
        return list(api_keys), total_count
    
    async def get_active_api_key_by_hash(self, key_hash: str) -> Optional[ApiKey]:
        """
        Get active API key by hash.
        
        Args:
            key_hash: Hashed API key
            
        Returns:
            Optional[ApiKey]: Active API key instance if found
        """
        query = select(ApiKey).where(
            and_(
                ApiKey.key_hash == key_hash,
                ApiKey.is_active == True
            )
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update_usage(self, api_key_id: int) -> bool:
        """
        Update API key usage statistics.
        
        Args:
            api_key_id: API key ID
            
        Returns:
            bool: True if updated successfully
        """
        query = (
            update(ApiKey)
            .where(ApiKey.id == api_key_id)
            .values(
                usage_count=ApiKey.usage_count + 1,
                last_used_at=func.now(),
                updated_at=func.now()
            )
        )
        
        result = await self.session.execute(query)
        return result.rowcount > 0
    
    async def deactivate_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Deactivate an API key.
        
        Args:
            api_key_id: API key ID
            user_id: Owner user ID (for security)
            
        Returns:
            bool: True if deactivated successfully
        """
        query = (
            update(ApiKey)
            .where(
                and_(
                    ApiKey.id == api_key_id,
                    ApiKey.user_id == user_id
                )
            )
            .values(
                is_active=False,
                updated_at=func.now()
            )
        )
        
        result = await self.session.execute(query)
        return result.rowcount > 0
    
    async def update_api_key(
        self,
        api_key_id: int,
        user_id: int,
        **kwargs
    ) -> Optional[ApiKey]:
        """
        Update an API key.
        
        Args:
            api_key_id: API key ID
            user_id: Owner user ID (for security)
            **kwargs: Fields to update
            
        Returns:
            Optional[ApiKey]: Updated API key instance
        """
        # Add updated_at timestamp
        kwargs["updated_at"] = func.now()
        
        query = (
            update(ApiKey)
            .where(
                and_(
                    ApiKey.id == api_key_id,
                    ApiKey.user_id == user_id
                )
            )
            .values(**kwargs)
        )
        
        result = await self.session.execute(query)
        
        if result.rowcount > 0:
            return await self.get_by_id(api_key_id)
        return None
    
    async def delete_api_key(self, api_key_id: int, user_id: int) -> bool:
        """
        Delete an API key.
        
        Args:
            api_key_id: API key ID
            user_id: Owner user ID (for security)
            
        Returns:
            bool: True if deleted successfully
        """
        api_key = await self.session.get(ApiKey, api_key_id)
        
        if api_key and api_key.user_id == user_id:
            await self.session.delete(api_key)
            return True
        
        return False
    
    async def count_user_api_keys(self, user_id: int, active_only: bool = True) -> int:
        """
        Count API keys for a user.
        
        Args:
            user_id: User ID
            active_only: Whether to count only active keys
            
        Returns:
            int: Number of API keys
        """
        conditions = [ApiKey.user_id == user_id]
        if active_only:
            conditions.append(ApiKey.is_active == True)
        
        query = select(func.count(ApiKey.id)).where(and_(*conditions))
        result = await self.session.execute(query)
        return result.scalar()
    
    async def get_expired_api_keys(self, limit: int = 100) -> List[ApiKey]:
        """
        Get expired API keys for cleanup.
        
        Args:
            limit: Maximum number of results
            
        Returns:
            List[ApiKey]: List of expired API keys
        """
        query = (
            select(ApiKey)
            .where(
                and_(
                    ApiKey.expires_at.is_not(None),
                    ApiKey.expires_at < func.now(),
                    ApiKey.is_active == True
                )
            )
            .limit(limit)
        )
        
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def cleanup_expired_keys(self) -> int:
        """
        Deactivate expired API keys.
        
        Returns:
            int: Number of keys deactivated
        """
        query = (
            update(ApiKey)
            .where(
                and_(
                    ApiKey.expires_at.is_not(None),
                    ApiKey.expires_at < func.now(),
                    ApiKey.is_active == True
                )
            )
            .values(
                is_active=False,
                updated_at=func.now()
            )
        )
        
        result = await self.session.execute(query)
        return result.rowcount
    
    async def search_api_keys(
        self,
        user_id: int,
        search_term: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[ApiKey], int]:
        """
        Search API keys with filters.
        
        Args:
            user_id: User ID
            search_term: Search term for name or prefix
            is_active: Filter by active status
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Tuple[List[ApiKey], int]: (api_keys, total_count)
        """
        conditions = [ApiKey.user_id == user_id]
        
        if search_term:
            search_filter = or_(
                ApiKey.name.ilike(f"%{search_term}%"),
                ApiKey.key_prefix.ilike(f"%{search_term}%")
            )
            conditions.append(search_filter)
        
        if is_active is not None:
            conditions.append(ApiKey.is_active == is_active)
        
        # Get total count
        count_query = select(func.count(ApiKey.id)).where(and_(*conditions))
        count_result = await self.session.execute(count_query)
        total_count = count_result.scalar()
        
        # Get paginated results
        query = (
            select(ApiKey)
            .where(and_(*conditions))
            .order_by(ApiKey.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(query)
        api_keys = result.scalars().all()
        
        return list(api_keys), total_count