"""
User registration service module.

This module contains business logic for user registration operations.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import constant_variable
from app.models.domain.user import UserDomain
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest
from app.utils.security import hash_password


class RegistrationService:
    """
    User registration service.
    
    Handles business logic for user registration.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize registration service.
        
        Args:
            session: Database session instance
        """
        self.user_repository = UserRepository(session)
    
    async def register(self, register_data: RegisterRequest) -> UserDomain:
        """
        Register a new user.
        
        Args:
            register_data: Registration request data
            
        Returns:
            UserDomain: Created user domain model
            
        Raises:
            HTTPException: If email or username already exists
        """
        # Check if email already exists
        if await self.user_repository.email_exists(register_data.email):
            raise HTTPException(
                status_code=constant_variable.HTTP_400_BAD_REQUEST,
                detail=constant_variable.AUTH_MESSAGES["EMAIL_EXISTS"]
            )
        
        # Check if username already exists
        if await self.user_repository.username_exists(register_data.username):
            raise HTTPException(
                status_code=constant_variable.HTTP_400_BAD_REQUEST,
                detail=constant_variable.AUTH_MESSAGES["USERNAME_EXISTS"]
            )
        
        # Hash password
        hashed_password = hash_password(register_data.password)
        
        # Create user
        user = await self.user_repository.create(
            email=register_data.email,
            username=register_data.username,
            hashed_password=hashed_password,
            full_name=register_data.full_name,
            is_active=True,
            is_verified=False
        )
        
        return UserDomain.from_orm(user)