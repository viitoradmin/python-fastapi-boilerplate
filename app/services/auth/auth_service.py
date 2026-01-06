"""
Main authentication service module.

This module provides a unified interface for all authentication operations.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.user import UserDomain
from app.schemas.auth import RegisterRequest, LoginRequest
from app.services.auth.registration_service import RegistrationService
from app.services.auth.login_service import LoginService
from app.services.auth.user_service import UserService


class AuthService:
    """
    Main authentication service.
    
    Provides a unified interface for authentication operations by delegating
    to specialized services.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize authentication service.
        
        Args:
            session: Database session instance
        """
        self.registration_service = RegistrationService(session)
        self.login_service = LoginService(session)
        self.user_service = UserService(session)
    
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
        return await self.registration_service.register(register_data)
    
    async def authenticate(self, login_data: LoginRequest) -> tuple[UserDomain, dict]:
        """
        Authenticate a user and return user with JWT tokens.
        
        Args:
            login_data: Login request data
            
        Returns:
            tuple[UserDomain, dict]: User domain model and JWT tokens
            
        Raises:
            HTTPException: If user not found or password incorrect
        """
        return await self.login_service.authenticate(login_data)
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserDomain]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[UserDomain]: User domain model if found, None otherwise
        """
        return await self.user_service.get_user_by_id(user_id)