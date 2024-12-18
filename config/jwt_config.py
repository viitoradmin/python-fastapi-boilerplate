"""
JWT Configuration Module for FastAPI

- This module manages configuration settings related to
JSON Web Tokens (JWT) in a FastAPI application.
- It provides information such as the issuer, token lifetime,
algorithm, and secret key used for token generation and verification.
"""

import datetime
import os

from dotenv import load_dotenv

load_dotenv()

# JWT info
JWT_LIFETIME = datetime.timedelta(days=7)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ.get("JWT_REFRESH_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
AUTHJWT_SECRET_KEY = os.environ.get("AUTHJWT_SECRET_KEY")
AUTHJWT_EXPIRES_TIME = bool(os.environ.get("THJWT_EXPIRES_TIME"))
