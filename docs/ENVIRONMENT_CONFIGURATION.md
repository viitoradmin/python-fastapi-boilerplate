# Environment Configuration Guide

This document explains how to configure environment variables for the FastAPI Boilerplate project across different environments (local, development, and production).

## Quick Start

1. **Copy the appropriate example file:**
   ```bash
   # For local development
   cp local.env.example local.env
   
   # For development/staging
   cp dev.env.example dev.env
   
   # For production
   cp production.env.example production.env
   ```

2. **Edit the copied file** with your actual configuration values

3. **Run the application** with the desired environment:
   ```bash
   # Local development
   python asgi.py --env local
   
   # Development/staging
   python asgi.py --env dev
   
   # Production
   python asgi.py --env prod
   ```

## Environment Files Overview

| File | Purpose | Security Level | Debug Mode |
|------|---------|----------------|------------|
| `local.env` | Local development | Low (convenience) | Enabled |
| `dev.env` | Development/Staging | Medium | Disabled |
| `production.env` | Production | High (strict) | Disabled |
| `env.example` | General template | N/A | Configurable |

## Configuration Sections

### 1. Server Configuration

Controls how the FastAPI server runs:

```env
SERVER_HOST=localhost          # Bind address (0.0.0.0 for external access)
SERVER_PORT=8008              # Port number
BASE_URL=http://localhost:8008 # Base URL for API responses
ENV=local                     # Environment type (local/dev/prod)
DEBUG=false                   # Enable debug mode
```

### 2. Database Configuration

MySQL database connection settings:

```env
DB_HOST=localhost             # Database server host
DB_PORT=3306                 # Database port
DB_USER=root                 # Database username
DB_PASSWORD=secure_password   # Database password
DB_NAME=fastapi_db           # Database name
DB_POOL_SIZE=10              # Connection pool size
DB_MAX_OVERFLOW=20           # Max overflow connections
DB_POOL_PRE_PING=true        # Enable connection health checks
DB_ECHO=false                # Log SQL queries (dev only)
```

### 3. Security Configuration

JWT and password security settings:

```env
JWT_SECRET_KEY=your-secret-key           # JWT signing key (MUST be secure in production)
JWT_ALGORITHM=HS256                      # JWT algorithm
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30       # Access token expiration
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7          # Refresh token expiration
PASSWORD_MIN_LENGTH=8                    # Minimum password length
PASSWORD_REQUIRE_UPPERCASE=true          # Require uppercase letters
PASSWORD_REQUIRE_LOWERCASE=true          # Require lowercase letters
PASSWORD_REQUIRE_NUMBERS=true            # Require numbers
PASSWORD_REQUIRE_SPECIAL_CHARS=true      # Require special characters
```

### 4. CORS Configuration

Cross-Origin Resource Sharing settings:

```env
CORS_ORIGINS=http://localhost:3000,https://yourapp.com  # Allowed origins
CORS_ALLOW_CREDENTIALS=true                             # Allow credentials
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS         # Allowed methods
CORS_ALLOW_HEADERS=*                                    # Allowed headers
```

### 5. Rate Limiting

API rate limiting configuration:

```env
RATE_LIMIT_ENABLED=true              # Enable rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=100   # Requests per minute limit
RATE_LIMIT_BURST_SIZE=10             # Burst size for rate limiting
```

### 6. Logging Configuration

Application logging settings:

```env
LOG_LEVEL=INFO                # Log level (DEBUG, INFO, WARNING, ERROR)
LOG_FORMAT=json              # Log format (json, text)
LOG_FILE_ENABLED=false       # Enable file logging
LOG_FILE_PATH=logs/app.log   # Log file path
LOG_ROTATION_SIZE=10MB       # Log rotation size
LOG_RETENTION_DAYS=30        # Log retention period
```

## Environment-Specific Recommendations

### Local Development (`local.env`)

- **Security**: Relaxed for convenience
- **Database**: Local MySQL instance
- **CORS**: Allow all localhost origins
- **Rate Limiting**: Disabled or very permissive
- **Logging**: DEBUG level, console output
- **Features**: All enabled for testing

```env
# Example local configuration
SERVER_HOST=localhost
SERVER_PORT=9000
DEBUG=true
DB_PASSWORD=                    # Empty for local dev
JWT_SECRET_KEY=local-dev-key    # Simple key for development
CORS_ORIGINS=*                  # Allow all origins
RATE_LIMIT_ENABLED=false        # Disable rate limiting
LOG_LEVEL=DEBUG                 # Verbose logging
```

### Development/Staging (`dev.env`)

- **Security**: Moderate security
- **Database**: Shared development database
- **CORS**: Specific development domains
- **Rate Limiting**: Moderate limits
- **Logging**: INFO level with file output
- **Features**: Most features enabled for testing

```env
# Example development configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=7000
DEBUG=false
DB_PASSWORD=secure_dev_password
JWT_SECRET_KEY=dev-environment-secret-key
CORS_ORIGINS=https://dev.yourapp.com,https://staging.yourapp.com
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=200
LOG_LEVEL=INFO
```

### Production (`production.env`)

- **Security**: Maximum security
- **Database**: Production database with connection pooling
- **CORS**: Strict domain restrictions
- **Rate Limiting**: Conservative limits
- **Logging**: WARNING level with rotation
- **Features**: Carefully selected production features

```env
# Example production configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=false
DB_PASSWORD=VERY_SECURE_PRODUCTION_PASSWORD
JWT_SECRET_KEY=CRYPTOGRAPHICALLY_SECURE_RANDOM_KEY
CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
LOG_LEVEL=WARNING
```

## Security Best Practices

### 1. Secret Management

- **Never commit real secrets** to version control
- Use **strong, random keys** for JWT secrets in production
- Consider using **environment variable injection** or **secret management services**
- **Rotate secrets regularly** in production

### 2. Database Security

- Use **strong passwords** for database connections
- **Limit database user permissions** to only required operations
- Enable **SSL/TLS** for database connections in production
- Use **connection pooling** to prevent connection exhaustion

### 3. CORS Configuration

- **Never use `*`** for CORS origins in production
- **Specify exact domains** that need access
- **Avoid credentials** with wildcard origins
- **Review and update** CORS settings regularly

### 4. Rate Limiting

- **Enable rate limiting** in all non-local environments
- **Set conservative limits** initially and adjust based on usage
- **Monitor rate limit hits** and adjust as needed
- **Consider different limits** for different endpoints

## Environment Variable Loading

The application loads environment variables in this order:

1. **System environment variables** (highest priority)
2. **Environment-specific `.env` file** (e.g., `local.env`, `dev.env`, `production.env`)
3. **Default values** in the code (lowest priority)

This allows for flexible configuration where system environment variables can override file-based configuration.

## Validation and Errors

The application validates critical environment variables on startup:

- **Database connection** is tested during startup
- **Invalid configuration** will prevent the application from starting
- **Missing required variables** will show clear error messages
- **Type validation** ensures numeric values are properly formatted

## Docker and Container Deployment

When deploying with Docker:

```dockerfile
# Copy environment file
COPY production.env /app/production.env

# Set environment
ENV ENV=prod

# Or use environment variables directly
ENV DB_HOST=prod-db.example.com
ENV DB_USER=prod_user
ENV JWT_SECRET_KEY=your-secure-key
```

## Monitoring and Health Checks

The application provides health check endpoints that report:

- **Environment configuration** status
- **Database connectivity**
- **External service** availability
- **Application** health metrics

Access health checks at:
- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed system status

## Troubleshooting

### Common Issues

1. **Port already in use**: Change `SERVER_PORT` in your environment file
2. **Database connection failed**: Verify `DB_*` settings and database availability
3. **CORS errors**: Check `CORS_ORIGINS` configuration
4. **Rate limit exceeded**: Adjust `RATE_LIMIT_*` settings or check client behavior

### Debug Mode

Enable debug mode for troubleshooting:

```env
DEBUG=true
LOG_LEVEL=DEBUG
DB_ECHO=true  # Log SQL queries
```

**Warning**: Never enable debug mode in production!

## Example Usage

```bash
# Start local development server
python asgi.py --env local --debug

# Start development server
python asgi.py --env dev

# Start production server
python asgi.py --env prod

# Override environment variables
ENV=prod DB_HOST=custom-db.com python asgi.py --env prod
```

## Additional Resources

- [FastAPI Configuration Documentation](https://fastapi.tiangolo.com/advanced/settings/)
- [Pydantic Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/)
- [Security Best Practices](./SECURITY_HEADERS.md)
- [Database Migration Guide](./DATABASE_MIGRATIONS.md)