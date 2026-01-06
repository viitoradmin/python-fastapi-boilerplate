"""
API Key usage service module.

This module contains business logic for API key usage tracking and statistics.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.api_key import ApiKeyRepository


class UsageService:
    """
    API Key usage service.
    
    Handles business logic for API key usage tracking and statistics.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize usage service.
        
        Args:
            session: Database session instance
        """
        self.api_key_repository = ApiKeyRepository(session)
    
    async def get_api_key_usage_stats(self, api_key_id: int, user_id: int) -> Optional[dict]:
        """
        Get usage statistics for an API key.
        
        Args:
            api_key_id: API key ID
            user_id: User ID
            
        Returns:
            Optional[dict]: Usage statistics if key found and owned by user
        """
        api_key = await self.api_key_repository.get_by_id(api_key_id)
        
        if not api_key or api_key.user_id != user_id:
            return None
        
        return {
            "api_key_id": api_key.id,
            "usage_count": api_key.usage_count,
            "last_used_at": api_key.last_used_at.isoformat() if api_key.last_used_at else None,
            "rate_limit": api_key.rate_limit,
            "current_hour_usage": 0,  # Would need Redis for real-time tracking
            "remaining_requests": api_key.rate_limit,
            "created_at": api_key.created_at.isoformat(),
            "is_active": api_key.is_active,
            "is_expired": api_key.is_expired
        }
    
    async def update_usage(self, api_key_id: int) -> bool:
        """
        Update usage statistics for an API key.
        
        Args:
            api_key_id: API key ID
            
        Returns:
            bool: True if updated successfully
        """
        return await self.api_key_repository.update_usage(api_key_id)
    
    async def get_user_usage_summary(self, user_id: int) -> dict:
        """
        Get usage summary for all user's API keys.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Usage summary statistics
        """
        api_keys, total_count = await self.api_key_repository.get_user_api_keys(user_id)
        
        active_count = sum(1 for key in api_keys if key.is_active)
        expired_count = sum(1 for key in api_keys if key.is_expired)
        total_usage = sum(key.usage_count for key in api_keys)
        
        return {
            "total_keys": total_count,
            "active_keys": active_count,
            "expired_keys": expired_count,
            "inactive_keys": total_count - active_count,
            "total_usage": total_usage,
            "average_usage": total_usage / total_count if total_count > 0 else 0
        }