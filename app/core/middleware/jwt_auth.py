"""
JWT authentication middleware and dependencies.

This module provides JWT authentication dependencies for FastAPI routes.
"""
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_db_session
from app.core.utils import constant_variable
from app.models.domain.user import UserDomain
from app.repositories.user import UserRepository
from app.utils.jwt_utils import get_user_id_from_access_token, decode_access_token


class JWTBearer(HTTPBearer):
    """
    Custom HTTPBearer for JWT authentication.
    
    Extracts JWT token from Authorization header with Bearer scheme.
    """
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """
        Extract JWT token from request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Optional[HTTPAuthorizationCredentials]: Credentials if found
        """
        credentials = await super().__call__(request)
        
        if credentials and credentials.scheme.lower() == "bearer":
            return credentials
        
        return None


# Global JWT bearer instance
jwt_bearer = JWTBearer(auto_error=True)
optional_jwt_bearer = JWTBearer(auto_error=False)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(jwt_bearer)
) -> int:
    """
    Dependency to get current user ID from JWT token.
    
    Args:
        credentials: JWT credentials from Authorization header
        
    Returns:
        int: Current user ID
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    if not credentials:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract user ID from token
    user_id = get_user_id_from_access_token(credentials.credentials)
    return user_id


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session)
) -> UserDomain:
    """
    Dependency to get current user from JWT token.
    
    Args:
        user_id: Current user ID from JWT token
        session: Database session
        
    Returns:
        UserDomain: Current user domain object
        
    Raises:
        HTTPException: If user not found
    """
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return UserDomain.from_orm(user)


async def get_optional_current_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_jwt_bearer)
) -> Optional[int]:
    """
    Dependency to optionally get current user ID from JWT token.
    
    Args:
        credentials: Optional JWT credentials from Authorization header
        
    Returns:
        Optional[int]: Current user ID if token is valid, None otherwise
    """
    if not credentials:
        return None
    
    try:
        user_id = get_user_id_from_access_token(credentials.credentials)
        return user_id
    except HTTPException:
        return None


async def get_optional_current_user(
    user_id: Optional[int] = Depends(get_optional_current_user_id),
    session: AsyncSession = Depends(get_db_session)
) -> Optional[UserDomain]:
    """
    Dependency to optionally get current user from JWT token.
    
    Args:
        user_id: Optional current user ID from JWT token
        session: Database session
        
    Returns:
        Optional[UserDomain]: Current user domain object if found, None otherwise
    """
    if not user_id:
        return None
    
    try:
        user_repository = UserRepository(session)
        user = await user_repository.get_by_id(user_id)
        
        if user and user.is_active:
            return UserDomain.from_orm(user)
    except Exception:
        pass
    
    return None


def verify_jwt_token(token: str) -> dict:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        dict: Decoded token payload
        
    Raises:
        HTTPException: If token is invalid
    """
    return decode_access_token(token)


async def require_active_user(
    current_user: UserDomain = Depends(get_current_user)
) -> UserDomain:
    """
    Dependency to ensure user is active.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        UserDomain: Active user domain object
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive"
        )
    
    return current_user


async def require_verified_user(
    current_user: UserDomain = Depends(get_current_user)
) -> UserDomain:
    """
    Dependency to ensure user is verified.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        UserDomain: Verified user domain object
        
    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=constant_variable.HTTP_403_FORBIDDEN,
            detail="User account is not verified"
        )
    
    return current_user


class JWTAuthRequired:
    """
    Class-based dependency for JWT authentication with custom requirements.
    """
    
    def __init__(self, require_verified: bool = False):
        """
        Initialize JWT auth requirement.
        
        Args:
            require_verified: Whether to require verified user
        """
        self.require_verified = require_verified
    
    async def __call__(
        self,
        current_user: UserDomain = Depends(get_current_user)
    ) -> UserDomain:
        """
        Validate user based on requirements.
        
        Args:
            current_user: Current user from JWT token
            
        Returns:
            UserDomain: Validated user domain object
            
        Raises:
            HTTPException: If user doesn't meet requirements
        """
        if self.require_verified and not current_user.is_verified:
            raise HTTPException(
                status_code=constant_variable.HTTP_403_FORBIDDEN,
                detail="User account must be verified"
            )
        
        return current_user


# Convenience instances
require_auth = JWTAuthRequired()
require_verified_auth = JWTAuthRequired(require_verified=True)