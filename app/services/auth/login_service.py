"""
User login service module.

This module contains business logic for user authentication operations.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import constant_variable
from app.models.domain.user import UserDomain
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password, check_needs_rehash, hash_password
from app.utils.jwt_utils import create_user_tokens


class LoginService:
    """
    User login service.
    
    Handles business logic for user authentication.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize login service.
        
        Args:
            session: Database session instance
        """
        self.user_repository = UserRepository(session)
    
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
        # Get user by email
        user = await self.user_repository.get_active_user_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=constant_variable.AUTH_MESSAGES["INVALID_CREDENTIALS"]
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=constant_variable.AUTH_MESSAGES["INVALID_CREDENTIALS"]
            )
        
        # Check if password hash needs updating (e.g., migrating from bcrypt to Argon2)
        if check_needs_rehash(user.hashed_password):
            # Rehash password with current Argon2 parameters
            new_hashed_password = hash_password(login_data.password)
            await self.user_repository.update_password(user.id, new_hashed_password)
        
        # Create JWT tokens
        tokens = create_user_tokens(user.id, user.email)
        
        return UserDomain.from_orm(user), tokens