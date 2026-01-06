from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config.database import db_config
from app.db.base import Base

# Import all your ORM models here so Alembic can detect them
from app.models.orm.user import User
from app.models.orm.api_key import ApiKey
# Add other models as you create them:
# from app.models.orm.other_model import OtherModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_sync_database_url() -> str:
    """
    Convert async database URL to synchronous URL for Alembic.
    
    Alembic needs a synchronous connection, so we convert
    mysql+aiomysql:// to mysql+pymysql://
    
    Returns:
        str: Synchronous database URL
    """
    async_url = db_config.get_database_url()
    # Replace aiomysql with pymysql for synchronous operations
    sync_url = async_url.replace("mysql+aiomysql://", "mysql+pymysql://")
    return sync_url


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use synchronous database URL for migrations
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Convert async URL to sync URL for Alembic
    sync_url = get_sync_database_url()
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = sync_url
    
    # Use synchronous engine for migrations
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
