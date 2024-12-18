"""
Cookie Signing Configuration Module for FastAPI

- This module manages configuration settings related to cookie
signing in a FastAPI application.
- It includes parameters such as the secret key used for signing
cookies and the algorithm for the cookie signature.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# # Secret key for signing cookies
SIGNIN_SECRET_KEY = os.environ.get("SIGNIN_SECRET_KEY")
ITSDANGEROUS_KEY = os.environ.get("ITSDANGEROUS_KEY")
RESET_KEY = os.environ.get("RESET_KEY")
