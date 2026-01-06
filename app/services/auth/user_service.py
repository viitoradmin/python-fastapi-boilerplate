"""
User service module.

This module contains business logic for user management operations.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.user import UserDomain
from app.repositories.user import UserRepository


class UserService:
    """
    User service.
    
    Handles business logic for user management operations.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize user service.
        
        Args:
            session: Database session instance
        """
        self.user_repository = UserRepository(session)
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserDomain]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[UserDomain]: User domain model if found, None otherwise
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        return UserDomain.from_orm(user)
    
    async def get_user_by_email(self, email: str) -> Optional[UserDomain]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[UserDomain]: User domain model if found, None otherwise
        """
        user = await self.user_repository.get_active_user_by_email(email)
        if not user:
            return None
        return UserDomain.from_orm(user)
    
    async def update_user_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Update user password.
        
        Args:
            user_id: User ID
            new_password_hash: New hashed password
            
        Returns:
            bool: True if updated successfully
        """
        return await self.user_repository.update_password(user_id, new_password_hash)