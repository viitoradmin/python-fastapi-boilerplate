"""
Database configuration module.

This module handles database connection settings and configuration for MySQL.
"""
import os
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def load_env_file(env: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.
    
    Loads environment variables from a file named {env}.env.
    If env is not provided, uses the ENV environment variable or defaults to "local".
    
    Args:
        env: Environment name (local, dev, prod). If None, uses ENV env var or "local"
    """
    if env is None:
        env = os.getenv("ENV", "local")
    
    env_file = Path(f"{env}.env")
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    # Only set if not already in environment (allows override)
                    if key not in os.environ:
                        os.environ[key] = value


class DatabaseConfig:
    """
    Database configuration class.
    
    Handles database connection settings from environment variables.
    Automatically loads .env file based on ENV environment variable.
    """
    
    def __init__(self, env: Optional[str] = None, load_env: bool = True) -> None:
        """
        Initialize database configuration from environment variables.
        
        Args:
            env: Environment name (local, dev, prod). If None, uses ENV env var or "local"
            load_env: Whether to load .env file. Defaults to True
        """
        if load_env:
            load_env_file(env=env)
        
        self.host: str = os.getenv("DB_HOST", "localhost")
        self.port: int = int(os.getenv("DB_PORT", "3306"))
        self.user: str = os.getenv("DB_USER", "root")
        self.password: str = os.getenv("DB_PASSWORD", "")
        self.database: str = os.getenv("DB_NAME", "fastapi_db")
        self.pool_size: int = int(os.getenv("DB_POOL_SIZE", "10"))
        self.max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
        self.pool_pre_ping: bool = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"
        self.echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"
    
    def get_database_url(self) -> str:
        """
        Construct MySQL database URL for async operations.
        
        Returns:
            str: Database connection URL
        """
        return (
            f"mysql+aiomysql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}?charset=utf8mb4"
        )


# Global database configuration instance
db_config = DatabaseConfig()

# Create async engine
engine = create_async_engine(
    db_config.get_database_url(),
    pool_size=db_config.pool_size,
    max_overflow=db_config.max_overflow,
    pool_pre_ping=db_config.pool_pre_ping,
    echo=db_config.echo,
    future=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncSession:
    """
    Dependency function to get database session.
    
    Yields:
        AsyncSession: Database session instance
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

