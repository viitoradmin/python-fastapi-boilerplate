import os
from enum import Enum
from pydantic_settings import BaseSettings
from starlette.config import Config

# Environment Variables
current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", ".env.example")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="Fast API Boilerplate")
    API_VERSION: str = config("API_VERSION", default="v1")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str| None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE_NAME", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class LLMSettings(BaseSettings):
    LLM_MODEL: str = config("LLM_MODEL", default=None)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")
    SERVER_HOST: str = config("SERVER_HOST", default=None)
    SERVER_PORT: str = config("SERVER_PORT", default=None)



class Constants:
    # Standard Response Status
    STATUS_SUCCESS = "success"       # 200 OK
    STATUS_FAIL = "fail"             # 400 Bad Request / 422 Unprocessable Entity
    STATUS_ERROR = "error"           # 500 Internal Server Error
    STATUS_NULL = None               # Used when no specific status is needed
    STATUS_TRUE = True               # Used for boolean success responses
    STATUS_FALSE = False             # Used for boolean failure responses

    # Additional Standard HTTP Status Codes
    STATUS_CREATED = "created"       # 201 Created
    STATUS_ACCEPTED = "accepted"     # 202 Accepted
    STATUS_NO_CONTENT = "no_content" # 204 No Content
    STATUS_BAD_REQUEST = "bad_request" # 400 Bad Request
    STATUS_UNAUTHORIZED = "unauthorized" # 401 Unauthorized
    STATUS_FORBIDDEN = "forbidden"   # 403 Forbidden
    STATUS_NOT_FOUND = "not_found"   # 404 Not Found
    STATUS_METHOD_NOT_ALLOWED = "method_not_allowed" # 405 Method Not Allowed
    STATUS_CONFLICT = "conflict"     # 409 Conflict
    STATUS_UNPROCESSABLE_ENTITY = "unprocessable_entity" # 422 Unprocessable Entity
    STATUS_TOO_MANY_REQUESTS = "too_many_requests" # 429 Too Many Requests



class Messages:
    # Standard Response Messages
    SUCCESS = "Operation completed successfully."
    FAIL = "The request could not be processed due to client error."
    ERROR = "An internal server error occurred."
    NULL = "No content available."
    # TRUE = "The operation was successful."
    # FALSE = "The operation failed."

    # Additional Standard HTTP Status Messages
    CREATED = "Resource has been created successfully."
    ACCEPTED = "Request has been accepted for processing."
    NO_CONTENT = "No content to return."
    BAD_REQUEST = "Invalid request. Please check your input and try again."
    UNAUTHORIZED = "Authentication required or failed."
    FORBIDDEN = "You do not have permission to access this resource."
    NOT_FOUND = "The requested resource could not be found."
    METHOD_NOT_ALLOWED = "The HTTP method used is not allowed for this endpoint."
    CONFLICT = "A conflict occurred with the current state of the resource."
    UNPROCESSABLE_ENTITY = "The request was well-formed but contains semantic errors."
    TOO_MANY_REQUESTS = "Too many requests have been sent in a short period."

    # Custom Messages for Specific Scenarios
    INVALID_DATA = "The provided data is invalid."
    MISSING_PARAMETERS = "Required parameters are missing from the request."
    TIMEOUT = "The request timed out."
    NOT_IMPLEMENTED = "This feature is not yet implemented."
    SERVICE_UNAVAILABLE = "The service is currently unavailable. Please try again later."



class Settings(
    AppSettings,
    LLMSettings,
    EnvironmentSettings,
    Constants,
    Messages
    ):
    pass


settings = Settings()