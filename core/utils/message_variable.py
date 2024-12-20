## Success message ##
SUCCESS_USER_CREATE = "User created successfully!"
SUCCESS_USER_UPDATE = "User updated successfully!"
SUCCESS_USER_DELETE = "User deleted successfully!"
SUCCESS_USER_LIST = "Successfully retrieved the list of users!"
SUCCESS_LOGIN = "Login successful!"
SUCCESS_LOGOUT = "Logout successful!"
SUCCESS_PASSWORD_CHANGED = "Password changed successfully!"
SUCCESS_VERIFICATION_SENT = "Verification email sent successfully!"
SUCCESS_OPERATION_COMPLETED = "Operation completed successfully!"
SUCCESS_FILE_UPLOADED = "File uploaded successfully!"
EMAIL_ALLREADY_EXISTS = "Email already exists!"
SUCCESS_USER_LOGIN = "User logged in successfully!"
SUCCESS_RESET_LINK = "User reset link sent successfully!"
SUCCESS_USER_VERIFIED = "User verified successfully!"
SUCCESS_USER_LOGGED_IN = "Logged in successfully!"
SUCCESS_OTP_SENT = "OTP sent successfully!"


## Error message ##
ERROR_USER_CREATE = "Error occurred while creating the user!"
ERROR_USER_LIST = "No user list found to retrieve!"
ERROR_LOGIN_FAILED = "Invalid username or password!"
ERROR_UNAUTHORIZED = "Unauthorized access!"
ERROR_FORBIDDEN = "You do not have permission to perform this action!"
ERROR_PASSWORD_MISMATCH = "Passwords do not match!"
ERROR_PASSWORD_RESET = "Error occurred while resetting the password!"
ERROR_FILE_UPLOAD = "Error occurred while uploading the file!"
ERROR_VALIDATION = "Validation failed. Please check the input!"
ERROR_INTERNAL_SERVER = "An internal server error occurred!"
GENERIC_ERROR = "An error ocured while saving data"
SOMETHING_WENT_WRONG = "Woops, something's not quite right, please try again!"
INVALID_USER_CREDENTIAL = "Invalid user credentials!"
INVALID_PROVIDER_TOKEN = "Invalid provider token!"
INVALID_OTP = "Invalid OTP!"
ERROR_USER_NOT_FOUND = "User not found!"
ERROR_INVALID_REQUEST_BODY = "Invalid request body!"
ERROR_SMS_SERVICE = "SMS service not found!"
ERROR_OTP_VERIFICATION = "OTP verification failed!"
ERROR_OTP_SEND = "Error sending OTP to user!"


## Info message ##
INFO_NO_RECORDS = "No records found!"
INFO_SESSION_EXPIRED = "Your session has expired. Please log in again!"
INFO_MAINTENANCE_MODE = "The system is under maintenance. Please try again later!"
INFO_PENDING_VERIFICATION = "Your email is pending verification!"
INFO_PASSWORD_COMPLEXITY = "Password must be at least 8 characters long and include a mix of letters, numbers, and special characters!"
INFO_DATA_SYNCED = "Data synced successfully!"

## Validation message ##
# Uses: VALIDATION_REQUIRED_FIELD.format("Username")
VALIDATION_REQUIRED_FIELD = "{} is a required field!"
VALIDATION_INVALID_FORMAT = "{} has an invalid format!"
VALIDATION_MIN_LENGTH = "{} must be at least {} characters long!"
VALIDATION_MAX_LENGTH = "{} cannot exceed {} characters!"
VALIDATION_UNIQUE_FIELD = "{} must be unique!"
VALIDATION_INVALID_EMAIL = "Invalid email address format!"
VALIDATION_INVALID_DATE = "Invalid date format. Use YYYY-MM-DD!"
VALIDATION_INVALID_FILE_TYPE = "Invalid file type. Allowed types are: {}!"
INVALID_AUTH_TOKEN = "Invalid authentication token!"
TOKEN_REQUIRED = "Token is required to perform this operation!"

## Generic error message ##
GENERAL_PROCESSING = "Processing your request. Please wait..."
GENERAL_TRY_AGAIN = "Something went wrong. Please try again!"
GENERAL_CONTACT_SUPPORT = "If the issue persists, contact support!"
GENERAL_SUCCESS = "Success!"
GENERAL_FAILURE = "Failed to complete the operation!"

## Authentication error message ##
AUTH_USER_REGISTERED = "User registered successfully!"
AUTH_USER_NOT_REGISTERED = "User registration failed!"
AUTH_INVALID_TOKEN = "Invalid authentication token!"
AUTH_TOKEN_EXPIRED = "Authentication token has expired!"
AUTH_ACCOUNT_LOCKED = (
    "Your account has been locked due to multiple failed login attempts!"
)
AUTH_ACCOUNT_DISABLED = "Your account is disabled. Contact support!"
AUTH_PASSWORD_RESET_SUCCESS = "Password reset successfully!"
AUTH_PASSWORD_RESET_FAILED = "Password reset failed!"
AUTH_EMAIL_ALREADY_EXISTS = "An account with this email already exists!"
AUTH_USERNAME_ALREADY_EXISTS = "Username is already taken!"

## Curd message ##
# Uses: CRUD_CREATE_SUCCESS.format("User")
CRUD_CREATE_SUCCESS = "{} created successfully!"
CRUD_CREATE_FAILURE = "Failed to create {}!"
CRUD_UPDATE_SUCCESS = "{} updated successfully!"
CRUD_UPDATE_FAILURE = "Failed to update {}!"
CRUD_DELETE_SUCCESS = "{} deleted successfully!"
CRUD_DELETE_FAILURE = "Failed to delete {}!"
CRUD_FETCH_SUCCESS = "{} retrieved successfully!"
CRUD_FETCH_FAILURE = "Failed to retrieve {}!"

## File handling ##
FILE_NOT_FOUND = "The requested file was not found!"
FILE_TOO_LARGE = "The file is too large to upload!"
FILE_TYPE_NOT_ALLOWED = "This file type is not allowed!"
FILE_DOWNLOAD_SUCCESS = "File downloaded successfully!"
FILE_DOWNLOAD_FAILURE = "Failed to download the file!"
FILE_UPLOAD_SUCCESS = "File uploaded successfully!"
FILE_UPLOAD_FAILURE = "Failed to upload the file!"

## Notification message ##
NOTIFICATION_SENT_SUCCESS = "Notification sent successfully!"
NOTIFICATION_SENT_FAILURE = "Failed to send notification!"
ALERT_HIGH_PRIORITY = "High-priority alert! Immediate action required!"
ALERT_LOW_PRIORITY = "Low-priority alert."

## System message ##
SYSTEM_BUSY = "The system is currently busy. Please try again later!"
SYSTEM_MAINTENANCE = "The system is under maintenance. Please check back later!"
SYSTEM_SHUTDOWN = "System is shutting down. Please save your work!"
SYSTEM_RESTART = "System is restarting. Please wait..."
SYSTEM_OVERLOADED = "The system is overloaded. Please try again in a few minutes!"

## Pagination message ##
PAGINATION_INVALID_PAGE = "Invalid page number!"
PAGINATION_PAGE_NOT_FOUND = "Requested page does not exist!"
PAGINATION_NO_MORE_RESULTS = "No more results to display!"
FILTER_INVALID_QUERY = "Invalid filter query!"
FILTER_NO_RESULTS = "No results match the filter criteria!"

## Session message ##
SESSION_STARTED = "Session started successfully!"
SESSION_EXPIRED = "Your session has expired. Please log in again!"
SESSION_TERMINATED = "Session terminated successfully!"
SESSION_INVALID = "Invalid session token!"

## API message ##
API_RATE_LIMIT_EXCEEDED = "Rate limit exceeded! Please try again later!"
API_INVALID_REQUEST = "Invalid API request!"
API_ENDPOINT_NOT_FOUND = "API endpoint not found!"
API_METHOD_NOT_ALLOWED = "HTTP method not allowed for this endpoint!"
API_MISSING_PARAMETERS = "Missing required parameters in the request!"
API_SUCCESS = "API request processed successfully!"
API_FAILURE = "API request failed!"

## Miscellaneous message ##
ACTION_NOT_ALLOWED = "You are not allowed to perform this action!"
DUPLICATE_ENTRY = "{} already exists!"
INSUFFICIENT_PERMISSIONS = (
    "You don't have sufficient permissions to perform this operation!"
)
UNEXPECTED_ERROR = "An unexpected error occurred. Please try again!"
OPERATION_TIMEOUT = "The operation timed out. Please try again later!"
RESOURCE_NOT_FOUND = "The requested resource could not be found!"
INVALID_INPUT = "The provided input is invalid!"
