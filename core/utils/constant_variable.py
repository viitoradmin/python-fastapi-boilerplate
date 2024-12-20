## Constant String ##

## Constants Status ##
STATUS_SUCCESS = "success"
STATUS_FAIL = "fail"
STATUS_ERROR = "error"
STATUS_NULL = None
STATUS_TRUE = True
STATUS_FALSE = False
API_V1 = "/v1"
API_V2 = "/v2"

## Constant Number ##
STATUS_ZERO = 0
STATUS_ONE = 1
STATUS_TWO = 2
STATUS_THREE = 3
STATUS_FOUR = 4
STATUS_FIVE = 5
STATUS_SIX = 6
STATUS_SEVEN = 7
STATUS_EIGHT = 8
STATUS_NINE = 9
STATUS_TEN = 10

# Http status code
STATUS_CODE_200 = 200
STATUS_CODE_202 = 202
STATUS_CODE_201 = 201
STATUS_CODE_204 = 204
STATUS_CODE_400 = 400
STATUS_CODE_401 = 401
STATUS_CODE_500 = 500

## Constant Date ##
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

## Constant API ##
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_XML = "application/xml"
AUTH_HEADER = "Authorization"
X_API_KEY_HEADER = "X-API-KEY"

## Database Constants ##
DB_TYPE_POSTGRESQL = "postgresql"
DB_TYPE_MYSQL = "mysql"
DB_TYPE_SQLITE = "sqlite"
DB_TYPE_ORACLE = "oracle"

## Constant User Roles ##
ROLE_ADMIN = "admin"
ROLE_USER = "user"
ROLE_GUEST = "guest"

## Constant Settings ##
MAX_RETRIES = 3
TIMEOUT_LIMIT = 30  # in seconds

## Pagination Constants ##
DEFAULT_PAGE_SIZE = 20
DEFAULT_PAGE_NUMBER = 1
MAX_PAGE_SIZE = 100

## Time and Date Constants ##
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7
DAYS_IN_YEAR = 365

## Regular Expressions Patterns ##
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
PHONE_NUMBER_REGEX = r"^\+?[1-9]\d{1,14}$"

## File Types ##
FILE_TYPE_TEXT = "text/plain"
FILE_TYPE_JSON = "application/json"
FILE_TYPE_CSV = "text/csv"
FILE_TYPE_PDF = "application/pdf"
FILE_TYPE_IMAGE_JPEG = "image/jpeg"
FILE_TYPE_IMAGE_PNG = "image/png"
FILE_TYPE_EXCEL = "application/vnd.ms-excel"
FILE_TYPE_MP4 = "video/mp4"
FILE_TYPE_MPEG = "audio/mpeg"

## Miscellaneous ##
MAX_FILE_SIZE_MB = 10
DEFAULT_LANGUAGE = "en"
TIMEZONE_UTC = "UTC"
TIMEZONE_EST = "US/Eastern"

# Rate limits
RATE_LIMIT = 100
TIME_WINDOW = 60

# Channel to send the messages
SMS_CHANNEL = "sms"
EMAIL_CHANNEL = "email"
