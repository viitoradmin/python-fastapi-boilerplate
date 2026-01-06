# 🔐 API Key Management System

This document provides comprehensive information about the API Key Management System integrated into the EveryCRED DCS API.

## 📋 Overview

The API Key Management System provides secure, scalable API key authentication and authorization capabilities following industry best practices. It supports fine-grained access control, rate limiting, IP restrictions, and comprehensive usage tracking.

## 🏗️ Architecture

### Core Components

1. **ORM Model** (`app/models/orm/api_key.py`)
   - Database representation with proper indexes
   - Relationships with User model
   - Built-in validation properties

2. **Domain Model** (`app/models/domain/api_key.py`)
   - Business logic representation
   - Scope and IP validation methods
   - Conversion utilities

3. **Repository Layer** (`app/repositories/api_key.py`)
   - Database operations
   - Query optimization
   - Batch operations

4. **Service Layer** (`app/services/api_key.py`)
   - Business logic implementation
   - Validation and security checks
   - Usage tracking

5. **API Routes** (`app/api/v1/routes/api_keys.py`, `app/api/v2/routes/api_keys.py`)
   - RESTful endpoints
   - Standard response format
   - Comprehensive error handling

6. **Middleware** (`app/core/middleware/api_key_auth.py`)
   - Authentication middleware
   - Rate limiting
   - Scope validation

7. **Utilities** (`app/utils/api_key.py`)
   - Key generation and validation
   - Security utilities
   - Format validation

## 🔑 API Key Format

API keys follow a structured format for security and identification:

```
ak_YYYYMMDD_<random_token>
```

- **Prefix**: `ak_` (API Key identifier)
- **Date**: `YYYYMMDD` (creation date for identification)
- **Token**: URL-safe random token (32 bytes, base64-encoded)

### Example
```
ak_20250105_dGhpcyBpcyBhIHNhbXBsZSBhcGkga2V5IHRva2Vu
```

## 🛡️ Security Features

### 1. Secure Storage
- API keys are hashed using Argon2id before storage
- Only key prefixes are stored in plaintext for identification
- Full keys are never logged or stored in plaintext

### 2. Access Control
- **Scopes**: Fine-grained permission system
- **IP Restrictions**: Limit access to specific IP addresses
- **Rate Limiting**: Configurable requests per hour
- **Expiration**: Optional expiration dates

### 3. Usage Tracking
- Request count tracking
- Last usage timestamps
- Rate limiting enforcement
- Usage analytics

## 📊 Database Schema

### API Keys Table

```sql
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    scopes TEXT,  -- JSON array of allowed scopes
    allowed_ips TEXT,  -- JSON array of allowed IP addresses
    rate_limit INTEGER NOT NULL DEFAULT 1000,
    last_used_at DATETIME,
    usage_count INTEGER NOT NULL DEFAULT 0,
    expires_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Indexes
- `idx_api_key_hash` (unique)
- `idx_api_key_prefix`
- `idx_api_key_user_id`
- `idx_api_key_active`
- `idx_api_key_expires`
- `idx_api_key_user_active` (composite)

## 🚀 API Endpoints

### Version 1 (Production Ready)

#### Create API Key
```http
POST /api/v1/api/keys/
Authorization: Bearer <jwt_access_token>
Content-Type: application/json

{
  "name": "My Application Key",
  "scopes": ["read", "write"],
  "allowed_ips": ["192.168.1.100", "10.0.0.50"],
  "rate_limit": 1000,
  "expires_at": "2025-12-31T23:59:59Z"
}
```

#### List API Keys
```http
GET /api/v1/api/keys/?page=1&per_page=20&active_only=true
Authorization: Bearer <jwt_access_token>
```

#### Get API Key Details
```http
GET /api/v1/api/keys/{api_key_id}
Authorization: Bearer <jwt_access_token>
```

#### Update API Key
```http
PUT /api/v1/api/keys/{api_key_id}
Authorization: Bearer <jwt_access_token>
Content-Type: application/json

{
  "name": "Updated Key Name",
  "is_active": true,
  "rate_limit": 2000
}
```

#### Delete API Key
```http
DELETE /api/v1/api/keys/{api_key_id}
Authorization: Bearer <jwt_access_token>
```

#### Revoke API Key
```http
POST /api/v1/api/keys/{api_key_id}/revoke
Authorization: Bearer <jwt_access_token>
```

#### Validate API Key
```http
POST /api/v1/api/keys/validate
Content-Type: application/json

{
  "api_key": "ak_20250105_...",
  "scope": "read",
  "ip_address": "192.168.1.100"
}
```

#### Get Usage Statistics
```http
GET /api/v1/api/keys/{api_key_id}/usage
Authorization: Bearer <jwt_access_token>
```

#### Search API Keys
```http
GET /api/v1/api/keys/search?q=search_term&active=true&page=1&per_page=20
Authorization: Bearer <jwt_access_token>
```

### Version 2 (Enhanced Features)

Version 2 includes all v1 endpoints plus:

#### Batch Operations
```http
POST /api/v2/api-keys/batch-operations?operation=revoke&confirm=true
Content-Type: application/json

{
  "api_key_ids": [1, 2, 3, 4, 5]
}
```

#### Enhanced Analytics
- Security recommendations
- Impact analysis
- Advanced filtering and sorting

## 🔐 Authentication Flow

The API key management system uses JWT (JSON Web Tokens) for authentication. Here's the complete authentication flow:

### 1. User Registration/Login

First, users need to authenticate to get a JWT access token:

```python
import requests

# Register a new user
register_response = requests.post(
    "http://localhost:8008/api/v1/auth/register",
    json={
        "email": "user@example.com",
        "username": "myusername",
        "password": "SecurePassword123!",
        "full_name": "John Doe"
    }
)

# Or login with existing credentials
login_response = requests.post(
    "http://localhost:8008/api/v1/auth/login",
    json={
        "email": "user@example.com",
        "password": "SecurePassword123!"
    }
)

# Extract tokens
tokens = login_response.json()["data"]["tokens"]
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]
```

### 2. Using JWT Token for API Key Management

All API key management operations require the JWT access token:

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Now you can manage API keys
response = requests.get(
    "http://localhost:8008/api/v1/api/keys/",
    headers=headers
)
```

### 3. JWT Token Structure

The JWT token contains the following claims:
- `sub`: User ID (subject)
- `email`: User email
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp
- `type`: Token type (access/refresh)

## 🔧 Usage Examples

### Authentication First

```python
import requests

# First, authenticate to get JWT token
login_response = requests.post(
    "http://localhost:8008/api/v1/auth/login",
    json={
        "email": "user@example.com",
        "password": "your_password"
    }
)

login_data = login_response.json()
access_token = login_data["data"]["tokens"]["access_token"]

# Set up headers with JWT token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
```

### Creating an API Key

```python
# Create API key (using JWT authentication)
response = requests.post(
    "http://localhost:8008/api/v1/api/keys/",
    headers=headers,
    json={
        "name": "Production API Key",
        "scopes": ["read", "write"],
        "rate_limit": 5000,
        "allowed_ips": ["203.0.113.1"]
    }
)

api_key_data = response.json()
api_key = api_key_data["data"]["api_key"]  # Store this securely!
```

### Using an API Key

```python
import requests

# Using Authorization header (recommended)
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(
    "http://localhost:8008/api/v1/protected-endpoint",
    headers=headers
)

# Alternative: X-API-Key header
headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

response = requests.get(
    "http://localhost:8008/api/v1/protected-endpoint",
    headers=headers
)
```

### Protecting Endpoints

#### Using JWT Authentication (for API key management)
```python
from fastapi import Depends
from app.core.middleware.jwt_auth import get_current_user_id, get_current_user

@app.get("/user-profile")
async def get_user_profile(
    current_user = Depends(get_current_user)
):
    return {"message": "User profile", "user": current_user}

@app.post("/api/keys")
async def create_api_key(
    create_data: ApiKeyCreateRequest,
    current_user_id: int = Depends(get_current_user_id)
):
    # API key creation logic using current_user_id from JWT
    pass
```

#### Using API Key Authentication (for API access)
```python
from fastapi import Depends
from app.core.middleware.api_key_auth import get_current_api_key, require_api_key_scope

@app.get("/protected")
async def protected_endpoint(
    api_key = Depends(get_current_api_key)
):
    return {"message": "Access granted", "user_id": api_key.user_id}

@app.post("/admin-only")
async def admin_endpoint(
    api_key = Depends(require_api_key_scope("admin"))
):
    return {"message": "Admin access granted"}
```

## ⚙️ Configuration

### Environment Variables

```bash
# API Key Settings
API_KEY_DEFAULT_RATE_LIMIT=1000
API_KEY_DEFAULT_EXPIRY_DAYS=365
API_KEY_MAX_KEYS_PER_USER=10
API_KEY_CLEANUP_INTERVAL_HOURS=24

# Rate Limiting (Redis)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
```

### Constants

```python
# app/core/utils/constant_variable.py
API_KEY_DEFAULTS = {
    "RATE_LIMIT": 1000,
    "EXPIRY_DAYS": 365,
    "MAX_KEYS_PER_USER": 10,
    "PREFIX": "ak_",
    "MIN_LENGTH": 35,
}
```

## 🔒 Security Best Practices

### For API Providers

1. **Secure Storage**
   - Never store API keys in plaintext
   - Use Argon2id for hashing
   - Implement proper key rotation

2. **Access Control**
   - Use scopes for fine-grained permissions
   - Implement IP restrictions when possible
   - Set appropriate rate limits

3. **Monitoring**
   - Track API key usage
   - Monitor for suspicious activity
   - Implement alerting for anomalies

4. **Lifecycle Management**
   - Set expiration dates
   - Regular cleanup of unused keys
   - Provide easy revocation

### For API Consumers

1. **Key Management**
   - Store keys in environment variables
   - Never commit keys to version control
   - Use secure key management systems

2. **Usage**
   - Use HTTPS for all requests
   - Implement proper error handling
   - Respect rate limits

3. **Security**
   - Rotate keys regularly
   - Monitor usage patterns
   - Revoke compromised keys immediately

## 📈 Rate Limiting

### Implementation

The system includes a built-in rate limiter with the following features:

- **Time Windows**: Hour, day, or custom intervals
- **Per-Key Limits**: Individual limits per API key
- **Distributed Support**: Redis backend for production
- **Graceful Degradation**: In-memory fallback

### Usage

```python
from app.core.middleware.api_key_auth import check_api_key_rate_limit

@app.get("/rate-limited")
async def rate_limited_endpoint(
    api_key = Depends(check_api_key_rate_limit)
):
    return {"message": "Within rate limit"}
```

## 🧪 Testing

### Unit Tests

```python
# Test API key generation
def test_generate_api_key():
    full_key, prefix, hash_key = generate_api_key()
    assert full_key.startswith("ak_")
    assert len(full_key) >= 35
    assert verify_api_key(full_key, hash_key)

# Test validation
def test_api_key_validation():
    validation = validate_api_key_format("ak_20250105_validtoken")
    assert validation is True
```

### Integration Tests

```python
# Test API key creation endpoint
async def test_create_api_key():
    response = await client.post(
        "/api/v1/api-keys/",
        json={"name": "Test Key", "rate_limit": 100},
        params={"user_id": 1}
    )
    assert response.status_code == 201
    assert "api_key" in response.json()["data"]
```

## 🚨 Troubleshooting

### Common Issues

1. **Invalid API Key Format**
   - Ensure key follows `ak_YYYYMMDD_token` format
   - Check for URL encoding issues

2. **Rate Limit Exceeded**
   - Check current usage against limit
   - Consider increasing rate limit
   - Implement exponential backoff

3. **IP Restrictions**
   - Verify client IP matches allowed IPs
   - Consider proxy/load balancer IP forwarding

4. **Scope Permissions**
   - Ensure API key has required scopes
   - Check scope configuration

### Debugging

```python
# Enable debug logging
import logging
logging.getLogger("app.services.api_key").setLevel(logging.DEBUG)

# Check API key details
api_key_service = ApiKeyService(session)
validation = await api_key_service.validate_api_key(
    api_key="your_key_here",
    required_scope="read"
)
print(f"Validation result: {validation}")
```

## 📚 Additional Resources

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Argon2 Password Hashing](https://argon2-cffi.readthedocs.io/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
- [Rate Limiting Strategies](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)

## 🤝 Contributing

When contributing to the API key management system:

1. Follow the existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Consider security implications
5. Follow the standard response format

## 📄 License

This API key management system is part of the EveryCRED DCS API and follows the same licensing terms.