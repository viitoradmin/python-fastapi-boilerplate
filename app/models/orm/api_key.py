"""
API Key ORM model.

This module contains the SQLAlchemy ORM model for API Key entity.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ApiKey(Base):
    """
    API Key ORM model.
    
    Represents an API key in the database with authentication and access control information.
    """
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, index=True, nullable=False)
    key_prefix = Column(String(20), index=True, nullable=False)  # First 8 chars for identification
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Access control
    is_active = Column(Boolean, default=True, nullable=False)
    scopes = Column(Text, nullable=True)  # JSON string of allowed scopes
    allowed_ips = Column(Text, nullable=True)  # JSON string of allowed IP addresses
    rate_limit = Column(Integer, default=1000, nullable=False)  # Requests per hour
    
    # Usage tracking
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    
    # Lifecycle
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    # Indexes for common queries
    __table_args__ = (
        Index("idx_api_key_hash", "key_hash"),
        Index("idx_api_key_prefix", "key_prefix"),
        Index("idx_api_key_user_id", "user_id"),
        Index("idx_api_key_active", "is_active"),
        Index("idx_api_key_expires", "expires_at"),
        Index("idx_api_key_user_active", "user_id", "is_active"),
    )
    
    def __repr__(self) -> str:
        """
        String representation of ApiKey instance.
        
        Returns:
            str: String representation
        """
        return f"<ApiKey(id={self.id}, name={self.name}, prefix={self.key_prefix}, user_id={self.user_id})>"
    
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