import hashlib
import os
from datetime import datetime

import pytz
from cryptography.fernet import Fernet
from fastapi import Request
from passlib.context import CryptContext
from slowapi.util import get_remote_address

from config import session_config


class PasswordUtils:
    """This class is used to manage password management"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str):
        """
        This function is used to hash password
        Arguments:
            password(str) : password argument of string format.

        Returns:
            Hash of the password
        """
        return self.pwd_context.hash(password)


class EnrytionDecrytionUtils:

    # Initialize Fernet for encryption
    FERNET_KEY = os.getenv(
        "FERNET_KEY", Fernet.generate_key()
    )  # For encrypting session data
    fernet = Fernet(FERNET_KEY)

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive session data."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive session data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()


class SessionUtils:

    def get_client_ip(self, request: Request) -> str:
        """Retrieve client IP from headers or remote address."""
        return get_remote_address(request)

    def generate_session_id(self, user_agent: str, ip: str) -> str:
        """Generates a session ID bound to user-agent and IP."""
        return hashlib.sha256(
            f"{session_config.SECRET_KEY}{user_agent}{ip}".encode()
        ).hexdigest()


class DateTimeUtils:

    def get_time(self):
        """Returns current datetime in default timezone India Standard Time"""
        timezone = "Asia/Kolkata"
        return datetime.now(pytz.timezone(timezone))
