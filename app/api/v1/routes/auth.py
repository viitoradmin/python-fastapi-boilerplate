"""
Authentication routes for API v1.

This module contains authentication endpoints with database integration.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_db_session
from app.core.responses import StandardResponse
from app.core.utils import constant_variable
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth import AuthService
from app.utils.jwt_utils import create_user_tokens

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(
    register_data: RegisterRequest,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Register a new user and return JWT tokens.
    
    Args:
        register_data: Registration request data
        session: Database session
        
    Returns:
        StandardResponse: Registration response with user data and JWT tokens
    """
    auth_service = AuthService(session)
    user = await auth_service.register(register_data)
    
    # Create JWT tokens for the new user
    tokens = create_user_tokens(user.id, user.email)
    
    response = StandardResponse.created(
        data={
            "user": {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified
            },
            "tokens": tokens
        },
        message=constant_variable.AUTH_MESSAGES["USER_REGISTERED"]
    )
    
    return response.make


@router.post("/login")
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_db_session)
):
    """
    Authenticate a user and return JWT tokens.
    
    Args:
        login_data: Login request data
        session: Database session
        
    Returns:
        StandardResponse: Authentication response with user data and JWT tokens
    """
    auth_service = AuthService(session)
    user, tokens = await auth_service.authenticate(login_data)
    
    response = StandardResponse.success(
        data={
            "user": {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified
            },
            "tokens": tokens
        },
        message=constant_variable.AUTH_MESSAGES["LOGIN_SUCCESSFUL"]
    )
    
    return response.make
