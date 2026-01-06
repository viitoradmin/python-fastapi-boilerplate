"""
User domain model.

This module contains the domain model for User entity.
"""
from datetime import datetime
from typing import Optional


class UserDomain:
    """
    User domain model.
    
    Represents a user in the business domain layer.
    """
    
    def __init__(
        self,
        id: int,
        email: str,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        is_verified: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        """
        Initialize User domain model.
        
        Args:
            id: User ID
            email: User email address
            username: Username
            hashed_password: Hashed password
            full_name: Full name
            is_active: Whether user is active
            is_verified: Whether user is verified
            created_at: Creation timestamp
            updated_at: Last update timestamp
        """
        self.id = id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.is_verified = is_verified
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_orm(cls, orm_user) -> "UserDomain":
        """
        Create domain model from ORM model.
        
        Args:
            orm_user: User ORM instance
            
        Returns:
            UserDomain: Domain model instance
        """
        return cls(
            id=orm_user.id,
            email=orm_user.email,
            username=orm_user.username,
            hashed_password=orm_user.hashed_password,
            full_name=orm_user.full_name,
            is_active=orm_user.is_active,
            is_verified=orm_user.is_verified,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at
        )
    
    def to_dict(self) -> dict:
        """
        Convert domain model to dictionary.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
