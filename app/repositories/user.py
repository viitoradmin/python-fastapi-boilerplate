"""
User repository module.

This module contains the user repository with authentication-specific queries.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.orm.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository with authentication-specific queries.
    
    Extends BaseRepository with user-specific database operations.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize user repository.
        
        Args:
            session: Database session instance
        """
        super().__init__(User, session)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email address
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        return await self.get_by_field("email", email)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            Optional[User]: User instance if found, None otherwise
        """
        return await self.get_by_field("username", username)
    
    async def email_exists(self, email: str) -> bool:
        """
        Check if email already exists.
        
        Args:
            email: Email address to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        return await self.exists_by_field("email", email)
    
    async def username_exists(self, username: str) -> bool:
        """
        Check if username already exists.
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if username exists, False otherwise
        """
        return await self.exists_by_field("username", username)
    
    async def get_active_user_by_email(self, email: str) -> Optional[User]:
        """
        Get active user by email address.
        
        Args:
            email: User email address
            
        Returns:
            Optional[User]: Active user instance if found, None otherwise
        """
        result = await self.session.execute(
            select(User)
            .where(User.email == email)
            .where(User.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def update_password(self, user_id: int, hashed_password: str) -> Optional[User]:
        """
        Update user password hash.
        
        Args:
            user_id: User ID
            hashed_password: New hashed password
            
        Returns:
            Optional[User]: Updated user instance if found, None otherwise
        """
        return await self.update(user_id, hashed_password=hashed_password)

