"""
Database initialization module.

This module provides functions to initialize the database and create tables.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.database import db_config
from app.db.base import Base
from app.models.orm.user import User


async def init_db() -> None:
    """
    Initialize database and create all tables.
    
    This function creates all database tables defined in the ORM models.
    """
    engine = create_async_engine(
        db_config.get_database_url(),
        echo=db_config.echo,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()


async def drop_db() -> None:
    """
    Drop all database tables.
    
    WARNING: This will delete all data in the database.
    """
    engine = create_async_engine(
        db_config.get_database_url(),
        echo=db_config.echo,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

