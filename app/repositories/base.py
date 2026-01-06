"""
Base repository module.

This module provides base repository class with common database operations
that can be reused across all repositories.
"""
from typing import Generic, Optional, TypeVar, Type, List, Any
from datetime import datetime

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository class with common database operations.
    
    Provides CRUD operations and common query methods that can be reused
    across all repositories.
    """
    
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """
        Initialize repository with model and session.
        
        Args:
            model: SQLAlchemy ORM model class
            session: Database session instance
        """
        self.model = model
        self.session = session
    
    async def create(self, **kwargs: Any) -> ModelType:
        """
        Create a new record in the database.
        
        Args:
            **kwargs: Model field values
            
        Returns:
            ModelType: Created model instance
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a record by its ID.
        
        Args:
            id: Record ID
            
        Returns:
            Optional[ModelType]: Model instance if found, None otherwise
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_field(
        self,
        field_name: str,
        field_value: Any,
        load_relationships: Optional[List[str]] = None
    ) -> Optional[ModelType]:
        """
        Get a record by a specific field value.
        
        Args:
            field_name: Name of the field to filter by
            field_value: Value to filter by
            load_relationships: Optional list of relationship names to eager load
            
        Returns:
            Optional[ModelType]: Model instance if found, None otherwise
        """
        query = select(self.model).where(
            getattr(self.model, field_name) == field_value
        )
        
        if load_relationships:
            for rel in load_relationships:
                query = query.options(selectinload(getattr(self.model, rel)))
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        Get all records with pagination and optional ordering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Field name to order by
            order_desc: Whether to order in descending order
            
        Returns:
            List[ModelType]: List of model instances
        """
        query = select(self.model)
        
        if order_by:
            order_field = getattr(self.model, order_by)
            if order_desc:
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field.asc())
        
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def update(self, id: int, **kwargs: Any) -> Optional[ModelType]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID
            **kwargs: Field values to update
            
        Returns:
            Optional[ModelType]: Updated model instance if found, None otherwise
        """
        # Add updated_at timestamp if field exists
        if hasattr(self.model, "updated_at"):
            kwargs["updated_at"] = datetime.utcnow()
        
        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
        )
        await self.session.flush()
        return await self.get_by_id(id)
    
    async def delete(self, id: int) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            bool: True if record was deleted, False if not found
        """
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.session.delete(instance)
        await self.session.flush()
        return True
    
    async def count(self) -> int:
        """
        Get total count of records.
        
        Returns:
            int: Total count of records
        """
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()
    
    async def exists(self, id: int) -> bool:
        """
        Check if a record exists by ID.
        
        Args:
            id: Record ID
            
        Returns:
            bool: True if record exists, False otherwise
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(self.model)
            .where(self.model.id == id)
        )
        return result.scalar_one() > 0
    
    async def exists_by_field(self, field_name: str, field_value: Any) -> bool:
        """
        Check if a record exists by field value.
        
        Args:
            field_name: Name of the field to check
            field_value: Value to check
            
        Returns:
            bool: True if record exists, False otherwise
        """
        result = await self.session.execute(
            select(func.count())
            .select_from(self.model)
            .where(getattr(self.model, field_name) == field_value)
        )
        return result.scalar_one() > 0

