"""
Constants module for the application.

This module contains all constant values used throughout the application.
"""

# Response status constants
STATUS_SUCCESS = "success"
STATUS_FAIL = "fail"
STATUS_ERROR = "error"

# HTTP status codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_429_TOO_MANY_REQUESTS = 429
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Success response codes (for determining status)
SUCCESS_STATUS_CODES = [HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED]

# Authentication messages
AUTH_MESSAGES = {
    "USER_REGISTERED": "User registered successfully",
    "LOGIN_SUCCESSFUL": "Login successful",
    "INVALID_CREDENTIALS": "Invalid email or password",
    "EMAIL_EXISTS": "Email already registered",
    "USERNAME_EXISTS": "Username already taken",
    "USER_NOT_FOUND": "User not found",
    "UNAUTHORIZED": "Unauthorized access",
}

# API Key messages
API_KEY_MESSAGES = {
    "CREATED": "API key created successfully",
    "UPDATED": "API key updated successfully",
    "DELETED": "API key deleted successfully",
    "REVOKED": "API key revoked successfully",
    "NOT_FOUND": "API key not found",
    "INVALID_KEY": "Invalid API key",
    "EXPIRED_KEY": "API key has expired",
    "INACTIVE_KEY": "API key is inactive",
    "RATE_LIMIT_EXCEEDED": "Rate limit exceeded for API key",
    "INSUFFICIENT_SCOPE": "API key does not have required scope",
    "IP_NOT_ALLOWED": "IP address not allowed for this API key",
    "INVALID_FORMAT": "Invalid API key format",
    "VALIDATION_SUCCESS": "API key is valid",
    "MAX_KEYS_REACHED": "Maximum number of API keys reached",
    "DUPLICATE_NAME": "API key name already exists",
}

# General messages
GENERAL_MESSAGES = {
    "HEALTH_OK": "Service is healthy",
    "VALIDATION_ERROR": "Validation failed",
    "INTERNAL_ERROR": "Internal server error",
    "NOT_FOUND": "Resource not found",
    "FORBIDDEN": "Access forbidden",
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
}

# Cookie settings
COOKIE_SETTINGS = {
    "HTTPONLY": False,
    "SECURE": False,  # Set to True in production with HTTPS
    "SAMESITE": "lax",
    "MAX_AGE": 60 * 60 * 24 * 30,  # 30 days
}

# Environment constants
ENV_LOCAL = "local"
ENV_DEV = "dev"
ENV_PROD = "prod"

# Database constants
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 0
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# API Key constants
API_KEY_DEFAULTS = {
    "RATE_LIMIT": 1000,  # Requests per hour
    "EXPIRY_DAYS": 365,  # Default expiry in days
    "MAX_KEYS_PER_USER": 10,  # Maximum API keys per user
    "PREFIX": "ak_",  # API key prefix
    "MIN_LENGTH": 35,  # Minimum API key length
}

# Rate limiting constants
RATE_LIMIT_WINDOWS = {
    "HOUR": 3600,  # 1 hour in seconds
    "DAY": 86400,  # 1 day in seconds
    "MINUTE": 60,  # 1 minute in seconds
}