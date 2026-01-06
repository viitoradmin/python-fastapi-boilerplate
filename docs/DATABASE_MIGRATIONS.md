# Database Migrations Guide

This guide covers using Alembic for database migrations in this FastAPI project.

## Overview

This project uses:
- **Database**: MySQL
- **ORM**: SQLAlchemy (async with `aiomysql`)
- **Migration Tool**: Alembic
- **Configuration**: Environment variables from `.env` files (`local.env`, `dev.env`, `production.env`)

## Configuration

### `app/db/migrations/env.py`

The migration environment is configured to use synchronous connections (Alembic requires sync, while the app uses async):

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config.database import db_config
from app.db.base import Base

# Import all your ORM models here so Alembic can detect them
from app.models.orm.user import User
# Add other models as you create them:
# from app.models.orm.other_model import OtherModel

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_sync_database_url() -> str:
    """
    Convert async database URL to synchronous URL for Alembic.
    
    Alembic needs a synchronous connection, so we convert
    mysql+aiomysql:// to mysql+pymysql://
    """
    async_url = db_config.get_database_url()
    sync_url = async_url.replace("mysql+aiomysql://", "mysql+pymysql://")
    return sync_url


def run_migrations_offline() -> None:
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
    sync_url = get_sync_database_url()
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = sync_url
    
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
```

**Important**: Always import all your ORM models in `env.py` so Alembic can detect schema changes.

### `alembic.ini`

The `sqlalchemy.url` in `alembic.ini` is set programmatically from environment variables in `env.py`. You can leave it empty or as a placeholder:

```ini
sqlalchemy.url = 
```

The actual database URL is loaded from your `.env` files via `db_config.get_database_url()`.

## Database Configuration

Database credentials are loaded from environment files. Update the appropriate `.env` file:

### `local.env`

```env
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "fastapi_db"
DB_POOL_SIZE = "10"
DB_MAX_OVERFLOW = "20"
DB_POOL_PRE_PING = "true"
DB_ECHO = "false"
```

### `dev.env` / `production.env`

Use the same structure with appropriate values for each environment.

**Note**: The `DatabaseConfig` class automatically loads the `.env` file based on the `ENV` environment variable (defaults to `"local"`).

## Prerequisites

1. **Install dependencies**:
   ```bash
   poetry add alembic pymysql
   ```

2. **Create the database**:
   ```sql
   CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Set environment variable** (optional, defaults to `local`):
   ```bash
   export ENV=local  # or dev, prod
   ```

## Migration Commands

### Create a New Migration

Generate a migration with autogenerate:

```bash
poetry run alembic revision --autogenerate -m "Description of your changes"
```

Example:
```bash
poetry run alembic revision --autogenerate -m "Add user table"
```

**Important**: Always review the generated migration file before applying it.

### Create an Empty Migration

Create an empty migration for manual SQL:

```bash
poetry run alembic revision -m "Description of your changes"
```

### Apply Migrations

Apply all pending migrations:

```bash
poetry run alembic upgrade head
```

Apply up to a specific revision:

```bash
poetry run alembic upgrade <revision_id>
```

### Rollback Migrations

Rollback one migration:

```bash
poetry run alembic downgrade -1
```

Rollback to a specific revision:

```bash
poetry run alembic downgrade <revision_id>
```

Rollback all migrations:

```bash
poetry run alembic downgrade base
```

### View Migration Status

Check current database revision:

```bash
poetry run alembic current
```

View migration history:

```bash
poetry run alembic history
```

View detailed history:

```bash
poetry run alembic history --verbose
```

### Preview SQL

Preview SQL that would be executed:

```bash
poetry run alembic upgrade head --sql
```

## Best Practices

### 1. Review Generated Migrations

Before applying autogenerated migrations:
- Verify all changes are expected
- Ensure no data loss will occur
- Check indexes and constraints are correct
- Verify foreign keys are properly handled

### 2. Use Descriptive Messages

```bash
# Good
poetry run alembic revision --autogenerate -m "Add email verification fields to users table"

# Bad
poetry run alembic revision --autogenerate -m "update"
```

### 3. Import All Models

Always import all ORM models in `app/db/migrations/env.py`:

```python
from app.models.orm.user import User
from app.models.orm.product import Product
from app.models.orm.order import Order
```

### 4. Test Before Production

1. Test on local database
2. Test on staging/dev environment
3. Backup production database before applying

### 5. Version Control

Always commit migration files to version control.

### 6. Environment Consistency

Use the same migration files across all environments. Only the database connection changes based on your `.env` files.

## Troubleshooting

### "Target database is not up to date"

Apply pending migrations:

```bash
poetry run alembic upgrade head
```

### "Can't locate revision identified by 'xyz'"

Check migration history:

```bash
poetry run alembic current
poetry run alembic history
```

### Autogenerate not detecting changes

**Solutions**:
- Ensure all models are imported in `env.py`
- Verify models inherit from `app.db.base.Base`
- Use migrations for all schema changes (don't modify database directly)

### Connection errors

**Solutions**:
- Verify database credentials in `.env` file
- Ensure database server is running
- Check database exists
- Verify `ENV` variable is set correctly

### MissingGreenlet error

**Solution**: Ensure `pymysql` is installed:

```bash
poetry add pymysql
```

### Migration conflicts

Merge branches:

```bash
poetry run alembic merge -m "Merge migrations" <revision1> <revision2>
```

## Quick Reference

### Common Workflow

1. Make changes to models in `app/models/orm/`
2. Generate migration:
   ```bash
   poetry run alembic revision --autogenerate -m "Description"
   ```
3. Review generated migration in `app/db/migrations/versions/`
4. Apply migration:
   ```bash
   poetry run alembic upgrade head
   ```
5. Commit migration files to version control

### Command Summary

```bash
# Create migration
poetry run alembic revision --autogenerate -m "message"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Check current revision
poetry run alembic current

# View history
poetry run alembic history

# Preview SQL
poetry run alembic upgrade head --sql
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL server hostname | `localhost` |
| `DB_PORT` | MySQL server port | `3306` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | `` (empty) |
| `DB_NAME` | Database name | `fastapi_db` |
| `DB_POOL_SIZE` | Connection pool size | `10` |
| `DB_MAX_OVERFLOW` | Max overflow connections | `20` |
| `DB_POOL_PRE_PING` | Enable connection health checks | `true` |
| `DB_ECHO` | Echo SQL queries (debug) | `false` |
| `ENV` | Environment name (local/dev/prod) | `local` |
