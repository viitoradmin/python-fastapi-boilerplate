"""
JWT utilities module.

This module provides functions for creating, validating, and decoding JWT tokens.
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from fastapi import HTTPException

from app.core.config.jwt_config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_TOKEN_EXPIRE_DAYS
)
from app.core.utils import constant_variable


class JWTManager:
    """
    JWT token management class.
    
    Handles creation, validation, and decoding of JWT tokens.
    """
    
    def __init__(self):
        """Initialize JWT manager with configuration."""
        # Use configuration from JWT config module
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JWT_ALGORITHM
        self.access_token_expire_minutes = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = JWT_REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Custom expiration time
            
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Data to encode in the token
            
        Returns:
            str: Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Dict[str, Any]: Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    def get_user_id_from_token(self, token: str) -> int:
        """
        Extract user ID from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            int: User ID
            
        Raises:
            HTTPException: If token is invalid or doesn't contain user_id
        """
        payload = self.decode_token(token)
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain user ID",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        try:
            return int(user_id)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=constant_variable.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"}
            )
    
    def verify_token_type(self, token: str, expected_type: str) -> bool:
        """
        Verify that token is of expected type.
        
        Args:
            token: JWT token
            expected_type: Expected token type (access, refresh)
            
        Returns:
            bool: True if token type matches
        """
        try:
            payload = self.decode_token(token)
            return payload.get("type") == expected_type
        except HTTPException:
            return False
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired without raising exception.
        
        Args:
            token: JWT token
            
        Returns:
            bool: True if token is expired
        """
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.JWTError:
            return True


# Global JWT manager instance
jwt_manager = JWTManager()


def create_user_tokens(user_id: int, email: str) -> Dict[str, str]:
    """
    Create access and refresh tokens for a user.
    
    Args:
        user_id: User ID
        email: User email
        
    Returns:
        Dict[str, str]: Dictionary with access_token and refresh_token
    """
    token_data = {
        "sub": str(user_id),
        "email": email
    }
    
    access_token = jwt_manager.create_access_token(token_data)
    refresh_token = jwt_manager.create_refresh_token({"sub": str(user_id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate an access token.
    
    Args:
        token: Access token to decode
        
    Returns:
        Dict[str, Any]: Token payload
        
    Raises:
        HTTPException: If token is invalid or not an access token
    """
    payload = jwt_manager.decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return payload


def get_user_id_from_access_token(token: str) -> int:
    """
    Extract user ID from access token.
    
    Args:
        token: Access token
        
    Returns:
        int: User ID
    """
    return jwt_manager.get_user_id_from_token(token)