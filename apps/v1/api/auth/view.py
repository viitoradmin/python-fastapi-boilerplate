"""This module is responsible to contain API's endpoint"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.v1.api.auth import schema
from apps.v1.api.auth.services import (
    user_login_service,
    social_login_service,
    user_signup_service,
    reset_password_service,
    forgot_password_service,
    email_verification_service,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from middleware import authentication_middleware
from config import db_config

## Load API's
authrouter = APIRouter()
getdb = db_config.get_db
oauth2_scheme = HTTPBearer()

## Define verison 1 API's here
class UsersAuthentication:
    """This class is for user's CRUD operation with version 1 API's"""

    @authrouter.post("/signup")
    async def signup_user(
        body: schema.CreateUser,
        db: AsyncSession = Depends(getdb)
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        response = await user_signup_service.UserAuthService().signup_user_service(
            db, body
        )
        return response

    @authrouter.post("/login")
    async def login_user(
        body: schema.LoginUser,
        db: AsyncSession = Depends(getdb),
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        response = await user_login_service.LoginService().login_user_service(db, body)
        return response

    @authrouter.post("/login/sso")
    async def login_sso_user(
        body: schema.LoginUser,
        db: AsyncSession = Depends(getdb),
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        response = await social_login_service.SsologinService().sso_login_user_service(
            db, body
        )
        return response

    @authrouter.post("/forgot/password")
    async def forgot_password(
        body: schema.ForgotPassword,
        db: AsyncSession = Depends(getdb),
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        response = await forgot_password_service.ForgotPasswordService().forgot_password_service(
            db, body
        )
        return response

    @authrouter.post("/reset/password")
    async def reset_password(
        body: schema.ResetPassword,
        db: AsyncSession = Depends(getdb),
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        response = (
            await reset_password_service.ResetPasswordService().reset_password_service(
                db, body
            )
        )
        return response

    @authrouter.post("/user/verification")
    async def user_verification(
        body: schema.EmailVerification,
        db: AsyncSession = Depends(getdb),
    ):
        """This API is for list user.
        Args: None
        Returns:
            response: will return users list."""
        current_users = AuthBackend().authenticate()
        response = await email_verification_service.EmailVerificationService().user_verification_service(
            db, body
        )
        return response
