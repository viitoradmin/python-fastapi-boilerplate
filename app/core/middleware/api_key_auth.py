"""
API Key authentication middleware.

This module provides middleware for API key authentication and authorization.
"""
from typing import Optional, Callable, List
import re

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.database import get_db_session
from app.core.utils import constant_variable
from app.services.api_key import ApiKeyService
from app.schemas.api_key import ApiKeyValidationResponse


class ApiKeyBearer(HTTPBearer):
    """
    Custom HTTPBearer for API key authentication.
    
    Extracts API key from Authorization header with Bearer scheme.
    """
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """
        Extract API key from request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Optional[HTTPAuthorizationCredentials]: Credentials if found
        """
        # First try Authorization header
        credentials = await super().__call__(request)
        
        if credentials:
            return credentials
        
        # Fallback to X-API-Key header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=api_key
            )
        
        # Fallback to query parameter (less secure, for development only)
        api_key = request.query_params.get("api_key")
        if api_key:
            return HTTPAuthorizationCredentials(
                scheme="Bearer",
                credentials=api_key
            )
        
        return None


# Global API key bearer instance
api_key_bearer = ApiKeyBearer(auto_error=False)


async def get_current_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(api_key_bearer),
    request: Request = None,
    session: AsyncSession = Depends(get_db_session)
) -> ApiKeyValidationResponse:
    """
    Dependency to get and validate current API key.
    
    Args:
        credentials: API key credentials
        request: FastAPI request object
        session: Database session
        
    Returns:
        ApiKeyValidationResponse: Validation result
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not credentials:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail=constant_variable.API_KEY_MESSAGES["INVALID_KEY"],
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get client IP
    client_ip = get_client_ip(request)
    
    # Validate API key
    api_key_service = ApiKeyService(session)
    validation_result = await api_key_service.validate_api_key(
        api_key=credentials.credentials,
        client_ip=client_ip
    )
    
    if not validation_result.is_valid:
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail=validation_result.error_message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return validation_result


async def get_optional_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(api_key_bearer),
    request: Request = None,
    session: AsyncSession = Depends(get_db_session)
) -> Optional[ApiKeyValidationResponse]:
    """
    Dependency to get and validate optional API key.
    
    Args:
        credentials: API key credentials
        request: FastAPI request object
        session: Database session
        
    Returns:
        Optional[ApiKeyValidationResponse]: Validation result if key provided
    """
    if not credentials:
        return None
    
    try:
        return await get_current_api_key(credentials, request, session)
    except HTTPException:
        return None


def require_api_key_scope(required_scope: str) -> Callable:
    """
    Dependency factory to require specific API key scope.
    
    Args:
        required_scope: Required scope for the endpoint
        
    Returns:
        Callable: Dependency function
    """
    async def check_scope(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(api_key_bearer),
        request: Request = None,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiKeyValidationResponse:
        """
        Check if API key has required scope.
        
        Args:
            credentials: API key credentials
            request: FastAPI request object
            session: Database session
            
        Returns:
            ApiKeyValidationResponse: Validation result
            
        Raises:
            HTTPException: If API key is invalid or lacks required scope
        """
        if not credentials:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=constant_variable.API_KEY_MESSAGES["INVALID_KEY"],
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Get client IP
        client_ip = get_client_ip(request)
        
        # Validate API key with required scope
        api_key_service = ApiKeyService(session)
        validation_result = await api_key_service.validate_api_key(
            api_key=credentials.credentials,
            required_scope=required_scope,
            client_ip=client_ip
        )
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=validation_result.error_message,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return validation_result
    
    return check_scope


def require_api_key_scopes(required_scopes: List[str]) -> Callable:
    """
    Dependency factory to require multiple API key scopes (any of them).
    
    Args:
        required_scopes: List of acceptable scopes
        
    Returns:
        Callable: Dependency function
    """
    async def check_scopes(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(api_key_bearer),
        request: Request = None,
        session: AsyncSession = Depends(get_db_session)
    ) -> ApiKeyValidationResponse:
        """
        Check if API key has any of the required scopes.
        
        Args:
            credentials: API key credentials
            request: FastAPI request object
            session: Database session
            
        Returns:
            ApiKeyValidationResponse: Validation result
            
        Raises:
            HTTPException: If API key is invalid or lacks any required scope
        """
        if not credentials:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=constant_variable.API_KEY_MESSAGES["INVALID_KEY"],
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Get client IP
        client_ip = get_client_ip(request)
        
        # Validate API key
        api_key_service = ApiKeyService(session)
        validation_result = await api_key_service.validate_api_key(
            api_key=credentials.credentials,
            client_ip=client_ip
        )
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail=validation_result.error_message,
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Check if API key has any of the required scopes
        if validation_result.scopes:
            has_scope = any(
                scope in validation_result.scopes or "*" in validation_result.scopes
                for scope in required_scopes
            )
            
            if not has_scope:
                raise HTTPException(
                    status_code=constant_variable.HTTP_403_FORBIDDEN,
                    detail=constant_variable.API_KEY_MESSAGES["INSUFFICIENT_SCOPE"]
                )
        
        return validation_result
    
    return check_scopes


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        str: Client IP address
    """
    # Check for forwarded headers (when behind proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        return forwarded_for.split(",")[0].strip()
    
    # Check for real IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    
    # Fallback to direct client IP
    if hasattr(request, "client") and request.client:
        return request.client.host
    
    return "unknown"


class ApiKeyRateLimiter:
    """
    Rate limiter for API keys.
    
    This is a simplified in-memory rate limiter.
    In production, use Redis or similar for distributed rate limiting.
    """
    
    def __init__(self):
        self._requests = {}  # {api_key_id: {window: count}}
    
    def is_rate_limited(
        self,
        api_key_id: int,
        rate_limit: int,
        window: str = "hour"
    ) -> bool:
        """
        Check if API key is rate limited.
        
        Args:
            api_key_id: API key ID
            rate_limit: Requests per window limit
            window: Time window
            
        Returns:
            bool: True if rate limited
        """
        from datetime import datetime
        
        current_time = datetime.utcnow()
        
        if window == "hour":
            time_key = current_time.strftime("%Y%m%d%H")
        else:
            time_key = current_time.strftime("%Y%m%d%H%M")
        
        key = f"{api_key_id}:{time_key}"
        
        current_count = self._requests.get(key, 0)
        
        if current_count >= rate_limit:
            return True
        
        # Increment counter
        self._requests[key] = current_count + 1
        
        # Clean up old entries (simple cleanup)
        if len(self._requests) > 10000:
            self._cleanup_old_entries()
        
        return False
    
    def _cleanup_old_entries(self):
        """Clean up old rate limiting entries."""
        from datetime import datetime, timedelta
        
        current_time = datetime.utcnow()
        cutoff_time = current_time - timedelta(hours=2)
        cutoff_key = cutoff_time.strftime("%Y%m%d%H")
        
        # Remove entries older than 2 hours
        keys_to_remove = [
            key for key in self._requests.keys()
            if key.split(":")[1] < cutoff_key
        ]
        
        for key in keys_to_remove:
            del self._requests[key]


# Global rate limiter instance
api_key_rate_limiter = ApiKeyRateLimiter()


async def check_api_key_rate_limit(
    validation_result: ApiKeyValidationResponse = Depends(get_current_api_key)
) -> ApiKeyValidationResponse:
    """
    Dependency to check API key rate limits.
    
    Args:
        validation_result: API key validation result
        
    Returns:
        ApiKeyValidationResponse: Validation result
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    if validation_result.is_valid and validation_result.api_key_id:
        is_limited = api_key_rate_limiter.is_rate_limited(
            api_key_id=validation_result.api_key_id,
            rate_limit=validation_result.rate_limit or constant_variable.API_KEY_DEFAULTS["RATE_LIMIT"]
        )
        
        if is_limited:
            raise HTTPException(
                status_code=constant_variable.HTTP_429_TOO_MANY_REQUESTS,
                detail=constant_variable.API_KEY_MESSAGES["RATE_LIMIT_EXCEEDED"]
            )
    
    return validation_result