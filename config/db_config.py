from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from config import env_config, redis_config, session_config
from core.utils import constant_variable

session_context: ContextVar[str] = ContextVar("session_context")


# ##### DATABASE CONFIGURATION ############################
SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{env_config.DATABASE_USER}:{env_config.DATABASE_PASSWORD}@{env_config.DATABASE_HOST}:{env_config.DATABASE_PORT}/{env_config.DATABASE_NAME}"


class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


engines = {
    EngineType.WRITER: create_async_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600),
    EngineType.READER: create_async_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600),
}


class RoutingSession(Session):
    def get_bind(
        self,
        mapper=constant_variable.STATUS_NULL,
        clause=constant_variable.STATUS_NULL,
        **kw,
    ):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=constant_variable.STATUS_FALSE,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=lambda: None,  # No `ContextVar`; manually handle Redis session.
)


class Base(DeclarativeBase): ...


@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = _async_session_factory()
    try:
        yield _session
    finally:
        await _session.close()


# Define FastAPI Dependencyasync def
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
