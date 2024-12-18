from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from core.utils import constant_variable, message_variable
from core.utils.token_authentication import JWTOAuth2
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import db_config

oauth2_scheme = HTTPBearer()
getdb = db_config.get_db


async def authenticate(
    authorize: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: AsyncSession = Depends(getdb),
):
    
    # TODO: Modify middleware as per requirement
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message_variable.INVALID_AUTH_TOKEN,
    )

    token_required_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message_variable.TOKEN_REQUIRED,
    )
    # try:

    token_data = JWTOAuth2().verify_access_token(
        authorize.credentials
    )  # This will raise an exception if the token is missing or invalid
    sub = token_data.get("sub")
    user_id = sub["id"]
    return user_id
