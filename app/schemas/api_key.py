"""
API Key schemas module.

This module contains Pydantic schemas for API key operations including
request/response models and validation.
"""
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class ApiKeyBase(BaseModel):
    """Base API key schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255, description="API key name")
    scopes: Optional[List[str]] = Field(None, description="List of allowed scopes")
    allowed_ips: Optional[List[str]] = Field(None, description="List of allowed IP addresses")
    rate_limit: int = Field(1000, ge=1, le=10000, description="Requests per hour limit")
    expires_at: Optional[datetime] = Field(None, description="Expiration date (optional)")


class ApiKeyCreateRequest(ApiKeyBase):
    """Schema for creating a new API key."""
    
    @validator('scopes')
    def validate_scopes(cls, v):
        """Validate scopes format."""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("Scopes must be a list")
            for scope in v:
                if not isinstance(scope, str) or not scope.strip():
                    raise ValueError("Each scope must be a non-empty string")
        return v
    
    @validator('allowed_ips')
    def validate_allowed_ips(cls, v):
        """Validate IP addresses format."""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("Allowed IPs must be a list")
            import ipaddress
            for ip in v:
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    raise ValueError(f"Invalid IP address: {ip}")
        return v
    
    @validator('expires_at')
    def validate_expires_at(cls, v):
        """Validate expiration date is in the future."""
        if v is not None:
            # Handle both timezone-aware and timezone-naive datetimes
            now = datetime.now(timezone.utc)
            
            # If the input datetime is timezone-naive, assume it's UTC
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            
            if v <= now:
                raise ValueError("Expiration date must be in the future")
        return v


class ApiKeyUpdateRequest(BaseModel):
    """Schema for updating an API key."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="API key name")
    is_active: Optional[bool] = Field(None, description="Whether the API key is active")
    scopes: Optional[List[str]] = Field(None, description="List of allowed scopes")
    allowed_ips: Optional[List[str]] = Field(None, description="List of allowed IP addresses")
    rate_limit: Optional[int] = Field(None, ge=1, le=10000, description="Requests per hour limit")
    expires_at: Optional[datetime] = Field(None, description="Expiration date (optional)")
    
    @validator('scopes')
    def validate_scopes(cls, v):
        """Validate scopes format."""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("Scopes must be a list")
            for scope in v:
                if not isinstance(scope, str) or not scope.strip():
                    raise ValueError("Each scope must be a non-empty string")
        return v
    
    @validator('allowed_ips')
    def validate_allowed_ips(cls, v):
        """Validate IP addresses format."""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("Allowed IPs must be a list")
            import ipaddress
            for ip in v:
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    raise ValueError(f"Invalid IP address: {ip}")
        return v
    
    @validator('expires_at')
    def validate_expires_at(cls, v):
        """Validate expiration date is in the future."""
        if v is not None:
            # Handle both timezone-aware and timezone-naive datetimes
            now = datetime.now(timezone.utc)
            
            # If the input datetime is timezone-naive, assume it's UTC
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            
            if v <= now:
                raise ValueError("Expiration date must be in the future")
        return v


class ApiKeyResponse(BaseModel):
    """Schema for API key response."""
    id: int = Field(..., description="API key ID")
    name: str = Field(..., description="API key name")
    key_prefix: str = Field(..., description="API key prefix for identification")
    user_id: int = Field(..., description="Owner user ID")
    is_active: bool = Field(..., description="Whether the API key is active")
    scopes: Optional[List[str]] = Field(None, description="List of allowed scopes")
    rate_limit: int = Field(..., description="Requests per hour limit")
    last_used_at: Optional[datetime] = Field(None, description="Last usage timestamp")
    usage_count: int = Field(..., description="Total usage count")
    expires_at: Optional[datetime] = Field(None, description="Expiration date")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    is_expired: bool = Field(..., description="Whether the API key is expired")
    is_valid: bool = Field(..., description="Whether the API key is valid")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ApiKeyCreateResponse(ApiKeyResponse):
    """Schema for API key creation response including the actual key."""
    api_key: str = Field(..., description="The actual API key (only shown once)")


class ApiKeyListResponse(BaseModel):
    """Schema for API key list response."""
    api_keys: List[ApiKeyResponse] = Field(..., description="List of API keys")
    total: int = Field(..., description="Total number of API keys")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    has_next: bool = Field(..., description="Whether there are more pages")


class ApiKeyUsageResponse(BaseModel):
    """Schema for API key usage statistics."""
    api_key_id: int = Field(..., description="API key ID")
    usage_count: int = Field(..., description="Total usage count")
    last_used_at: Optional[datetime] = Field(None, description="Last usage timestamp")
    rate_limit: int = Field(..., description="Requests per hour limit")
    current_hour_usage: int = Field(..., description="Usage in current hour")
    remaining_requests: int = Field(..., description="Remaining requests in current hour")


class ApiKeyValidationRequest(BaseModel):
    """Schema for API key validation request."""
    api_key: str = Field(..., description="API key to validate")
    scope: Optional[str] = Field(None, description="Required scope")
    ip_address: Optional[str] = Field(None, description="Client IP address")


class ApiKeyValidationResponse(BaseModel):
    """Schema for API key validation response."""
    is_valid: bool = Field(..., description="Whether the API key is valid")
    api_key_id: Optional[int] = Field(None, description="API key ID if valid")
    user_id: Optional[int] = Field(None, description="User ID if valid")
    scopes: Optional[List[str]] = Field(None, description="Available scopes")
    rate_limit: Optional[int] = Field(None, description="Rate limit")
    remaining_requests: Optional[int] = Field(None, description="Remaining requests")
    error_message: Optional[str] = Field(None, description="Error message if invalid")