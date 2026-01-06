"""
API Key domain model.

This module contains the domain model for API Key entity used in business logic.
"""
from datetime import datetime, timezone
from typing import Optional, List
from dataclasses import dataclass

from app.models.orm.api_key import ApiKey


@dataclass
class ApiKeyDomain:
    """
    API Key domain model.
    
    Represents an API key in the business logic layer with all necessary attributes
    and methods for API key operations.
    """
    id: int
    name: str
    key_prefix: str
    user_id: int
    is_active: bool
    scopes: Optional[List[str]]
    allowed_ips: Optional[List[str]]
    rate_limit: int
    last_used_at: Optional[datetime]
    usage_count: int
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_orm(cls, api_key: ApiKey) -> "ApiKeyDomain":
        """
        Create domain model from ORM model.
        
        Args:
            api_key: API key ORM model instance
            
        Returns:
            ApiKeyDomain: Domain model instance
        """
        import json
        
        # Parse JSON fields
        scopes = None
        if api_key.scopes:
            try:
                scopes = json.loads(api_key.scopes)
            except (json.JSONDecodeError, TypeError):
                scopes = []
        
        allowed_ips = None
        if api_key.allowed_ips:
            try:
                allowed_ips = json.loads(api_key.allowed_ips)
            except (json.JSONDecodeError, TypeError):
                allowed_ips = []
        
        return cls(
            id=api_key.id,
            name=api_key.name,
            key_prefix=api_key.key_prefix,
            user_id=api_key.user_id,
            is_active=api_key.is_active,
            scopes=scopes,
            allowed_ips=allowed_ips,
            rate_limit=api_key.rate_limit,
            last_used_at=api_key.last_used_at,
            usage_count=api_key.usage_count,
            expires_at=api_key.expires_at,
            created_at=api_key.created_at,
            updated_at=api_key.updated_at
        )
    
    @property
    def is_expired(self) -> bool:
        """
        Check if the API key is expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if self.expires_at is None:
            return False
        now = datetime.now(timezone.utc)
        expires_at = self.expires_at
        
        # Handle timezone-naive expiration dates
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        return now > expires_at
    
    @property
    def is_valid(self) -> bool:
        """
        Check if the API key is valid (active and not expired).
        
        Returns:
            bool: True if valid, False otherwise
        """
        return self.is_active and not self.is_expired
    
    def has_scope(self, required_scope: str) -> bool:
        """
        Check if the API key has a specific scope.
        
        Args:
            required_scope: The scope to check for
            
        Returns:
            bool: True if scope is allowed, False otherwise
        """
        if self.scopes is None:
            return True  # No scope restrictions
        return required_scope in self.scopes or "*" in self.scopes
    
    def is_ip_allowed(self, ip_address: str) -> bool:
        """
        Check if an IP address is allowed to use this API key.
        
        Args:
            ip_address: The IP address to check
            
        Returns:
            bool: True if IP is allowed, False otherwise
        """
        if self.allowed_ips is None or not self.allowed_ips:
            return True  # No IP restrictions
        return ip_address in self.allowed_ips
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Convert domain model to dictionary.
        
        Args:
            include_sensitive: Whether to include sensitive information
            
        Returns:
            dict: Dictionary representation
        """
        data = {
            "id": self.id,
            "name": self.name,
            "key_prefix": self.key_prefix,
            "user_id": self.user_id,
            "is_active": self.is_active,
            "scopes": self.scopes,
            "rate_limit": self.rate_limit,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "usage_count": self.usage_count,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_expired": self.is_expired,
            "is_valid": self.is_valid
        }
        
        if include_sensitive:
            data["allowed_ips"] = self.allowed_ips
        
        return data