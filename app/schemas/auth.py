"""
Authentication schemas.

This module contains Pydantic schemas for authentication operations.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Schema for login request.
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class RegisterRequest(BaseModel):
    """
    Schema for registration request.
    """
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")


class TokenResponse(BaseModel):
    """
    Schema for token response.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class AuthResponse(BaseModel):
    """
    Schema for authentication response.
    """
    message: str = Field(..., description="Response message")
    user_id: Optional[int] = Field(None, description="User ID")
