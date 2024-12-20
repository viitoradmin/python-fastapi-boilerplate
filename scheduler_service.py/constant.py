import datetime as dt
from datetime import datetime, timedelta, timezone

import pytz

# API response status
STATUS_SUCCESS = "success"
STATUS_FAIL = "fail"
STATUS_ERROR = "error"

# Hours
# FOUR = datetime.time(4, 00, 00)
# FOUR = dt.timedelta(11, 34, 59)

# Boolean status code
STATUS_ZERO = 0
STATUS_DOUBLEZERO = 00
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
TWELVE = 12
TWENTY_TWO = 22
THIRTY = 30
ONE_TWENTY = 120
STATUS_TRUE = True
STATUS_FALSE = False
STATUS_NULL = None

# Entity status
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_PUBLISHED = "published"
STATUS_UNPUBLISHED = "unpublished"
STATUS_CREATE = "create"
STATUS_UPDATE = "update"
STATUS_DELETE = "delete"
STATUS_ALL = "all"
STATUS_NEW = "new"

# Image upload path
REQUEST_LETTER_UPLOAD_PATH = "/letters/"

# Activity log action
INSERT_LOG = "insert"
UPDATE_LOG = "update"
DELETE_LOG = "delete"
SEND_FOR_APPROVAL_LOG = "send_for_approval"

# Roles
ROLE_SUPERADMIN = "superadmin"
ROLE_ADMIN = "admin"
ROLE_RECEPTIONIST = "receptionist"
ROLE_USER = "user"
ROLE_STAFF = "staff"

# Database
BASE_CONFIG_NAME = "base"
DEVELOPMENT_CONFIG_NAME = "development"
PRODUCTION_CONFIG_NAME = "production"
TEST_CONFIG_NAME = "test"

# Http status code
STATUS_CODE_200 = 200
STATUS_CODE_201 = 201
STATUS_CODE_204 = 204
STATUS_CODE_400 = 400
STATUS_CODE_401 = 401
STATUS_CODE_500 = 500

# API version prefix
API_V1 = "v1"
API_V2 = "v2"

# DateTime

# Channel to send the messages
SMS_CHANNEL = "sms"
EMAIL_CHANNEL = "email"

PERCENTAGE = "percentage"
FLAT = "flat"
