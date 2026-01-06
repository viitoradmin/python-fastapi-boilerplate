##  Standard Response System Documentation

This document explains the standardized response format implemented across the EveryCRED DCS API.

##  Overview

The Standard Response System provides a consistent API response format across all endpoints, ensuring predictable client interactions and proper error handling.

##  Response Format

All API responses follow this standard structure:

```json
{
  "status": "success|fail|error",
  "data": {}, // or null
  "message": "Human readable message"
}
```

### Status Types

- **`success`**: HTTP 2xx responses (200, 201, 202)
- **`fail`**: HTTP 4xx responses (400, 401, 404, etc.) - Client errors
- **`error`**: HTTP 5xx responses (500, 502, etc.) - Server errors

##  Implementation

### Using StandardResponse Class

```python
from app.core.responses import StandardResponse

# Success response
response = StandardResponse.success(
    data={"user_id": 123},
    message="User created successfully"
)
return response.make

# Created response (201)
response = StandardResponse.created(
    data={"user_id": 123},
    message="User registered successfully"
)
return response.make

# Error responses
response = StandardResponse.bad_request(
    message="Email already exists"
)
return response.make
```

### Available Methods

#### Success Responses
- `StandardResponse.success()` - 200 OK
- `StandardResponse.created()` - 201 Created

#### Client Error Responses
- `StandardResponse.bad_request()` - 400 Bad Request
- `StandardResponse.unauthorized()` - 401 Unauthorized
- `StandardResponse.forbidden()` - 403 Forbidden
- `StandardResponse.not_found()` - 404 Not Found
- `StandardResponse.conflict()` - 409 Conflict
- `StandardResponse.validation_error()` - 422 Unprocessable Entity

#### Server Error Responses
- `StandardResponse.internal_error()` - 500 Internal Server Error

## 🔍 Examples

### 1. Successful User Registration

**Request:**
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "user_id": 123,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false
  },
  "message": "User registered successfully"
}
```

### 2. Validation Error

**Request:**
```bash
POST /api/v1/auth/register
{
  "email": "invalid-email",
  "username": "",
  "password": "123"
}
```

**Response:**
```json
{
  "status": "fail",
  "data": {
    "errors": [
      {
        "field": "email",
        "message": "field required",
        "type": "value_error.missing"
      },
      {
        "field": "username",
        "message": "ensure this value has at least 1 characters",
        "type": "value_error.any_str.min_length"
      }
    ]
  },
  "message": "Validation failed"
}
```

### 3. Authentication Error

**Request:**
```bash
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "wrongpassword"
}
```

**Response:**
```json
{
  "status": "fail",
  "data": null,
  "message": "Invalid email or password"
}
```

### 4. Health Check

**Request:**
```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "service": "EveryCRED DCS API v1",
    "version": "1.0.0",
    "environment": "local",
    "timestamp": "2024-01-01T12:00:00.000000",
    "uptime": "healthy",
    "features": {
      "authentication": "enabled",
      "argon2_hashing": "enabled",
      "security_headers": "enabled",
      "rate_limiting": "enabled"
    }
  },
  "message": "Service is healthy"
}
```

## 🛠️ Error Handling

### Global Error Middleware

The system includes comprehensive error handling:

1. **HTTP Exceptions**: Automatically formatted with proper status codes
2. **Validation Errors**: Detailed field-level error information
3. **Unhandled Exceptions**: Logged and returned as internal server errors

### Custom Error Messages

Error messages are centralized in constants:

```python
# app/core/utils/constant_variable.py
AUTH_MESSAGES = {
    "USER_REGISTERED": "User registered successfully",
    "LOGIN_SUCCESSFUL": "Login successful",
    "INVALID_CREDENTIALS": "Invalid email or password",
    "EMAIL_EXISTS": "Email already registered",
    "USERNAME_EXISTS": "Username already taken",
}
```

## 🍪 Cookie Management

The StandardResponse class supports automatic cookie management:

```python
response = StandardResponse.success(
    data={"user_id": 123},
    message="Login successful",
    cookies={
        "session_token": "abc123",
        "user_preference": "dark_mode"
    }
)
```

Cookie settings are configurable in constants:
- `httponly`: False (configurable)
- `secure`: False (set to True in production)
- `samesite`: "lax"
- `max_age`: 30 days

## 📊 Status Code Mapping

| HTTP Code | Status Type | Usage |
|-----------|-------------|-------|
| 200 | success | Standard successful response |
| 201 | success | Resource created |
| 202 | success | Request accepted |
| 400 | fail | Bad request/validation error |
| 401 | fail | Authentication required |
| 403 | fail | Access forbidden |
| 404 | fail | Resource not found |
| 409 | fail | Resource conflict |
| 422 | fail | Validation error |
| 500 | error | Internal server error |

## 🔧 Configuration

### Constants Location
- **Response Constants**: `app/core/utils/constant_variable.py`
- **Standard Response**: `app/core/responses/standard_response.py`
- **Error Handlers**: `app/core/middleware/error_handler.py`

### Environment-Specific Behavior

**Development/Local:**
- Detailed error messages
- Full stack traces in logs
- Validation error details

**Production:**
- Generic error messages for security
- No sensitive information exposure
- Comprehensive logging

## 🚀 Migration Guide

### From Old Response Format

**Old Format:**
```python
return {"message": "Success", "user_id": 123}
```

**New Format:**
```python
response = StandardResponse.success(
    data={"user_id": 123},
    message="Success"
)
return response.make
```

### Exception Handling

**Old Format:**
```python
raise HTTPException(status_code=400, detail="Error message")
```

**New Format:**
```python
from app.core.utils import constant_variable

raise HTTPException(
    status_code=constant_variable.HTTP_400_BAD_REQUEST,
    detail=constant_variable.AUTH_MESSAGES["EMAIL_EXISTS"]
)
```

## 📈 Benefits

1. **Consistency**: All endpoints return the same format
2. **Predictability**: Clients know what to expect
3. **Error Handling**: Comprehensive error information
4. **Maintainability**: Centralized response logic
5. **Documentation**: Clear API contracts
6. **Testing**: Easier to validate responses
7. **Monitoring**: Standardized logging and metrics

## 🔍 Testing

### Example Test Cases

```python
def test_successful_response():
    response = StandardResponse.success(
        data={"test": "data"},
        message="Test successful"
    )
    json_response = response.make
    
    assert json_response.status_code == 200
    assert json_response.body["status"] == "success"
    assert json_response.body["data"]["test"] == "data"
    assert json_response.body["message"] == "Test successful"

def test_error_response():
    response = StandardResponse.bad_request(
        message="Test error"
    )
    json_response = response.make
    
    assert json_response.status_code == 400
    assert json_response.body["status"] == "fail"
    assert json_response.body["message"] == "Test error"
```

## 📚 Related Documentation

- [API Documentation URLs](./API_DOCUMENTATION_URLS.md)
- [Security Headers](./SECURITY_HEADERS.md)
- [Authentication System](../app/services/auth.py)

---

**Note**: This standard response system is automatically applied to all endpoints. No additional configuration is required for new endpoints when following the established patterns.