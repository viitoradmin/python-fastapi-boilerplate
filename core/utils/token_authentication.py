"""This module defines classes and methods for OAuth2
authentication and token management.

It contains a class `JWTOAuth2` with methods for generating access and
refresh tokens, encoding and decoding reset password and email confirmation tokens,
and verifying access tokens.
"""

import datetime
import os
import jwt
from fastapi import APIRouter, status
from config import project_path
from core.utils.standard_response import StandardResponse
from config import jwt_config, signing_cookies
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

oauth2router = APIRouter(tags="JWTOAuth2")
# Initialization for encoding
key = URLSafeTimedSerializer(signing_cookies.ITSDANGEROUS_KEY)
BACKEND_URL = os.environ.get("BACKEND_URL")


class JWTOAuth2:
    """Class for JWT-based OAuth2 authentication and token management."""

    def encode_access_token(self, identity: dict):
        """
        Generates the Auth Token

        Args:
            identity (tuple): Identity of the token to be decoded

        Returns:
            JWT Token string
        """
        try:
            now = datetime.datetime.now()
            exp_time = (
                now + jwt_config.JWT_LIFETIME
            )  # Assuming JWT_LIFETIME is a timedelta

            payload = {
                "iss": "Your-Issuer",  # Set your issuer here
                "exp": exp_time.timestamp(),  # Convert to timestamp
                "iat": now.timestamp(),  # Created date of token
                "sub": identity,  # The subject of the token (the user whom it identifies)
            }

            return jwt.encode(
                payload,
                signing_cookies.SIGNIN_SECRET_KEY,
                algorithm=jwt_config.JWT_ALGORITHM,
            )
        except:
            return StandardResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data=None,
                message="Failed to encode!",
            ).make

    def verify_access_token(self, token):
        """Verify the validity of an access token.

        Args:
            token (str): The access token to verify.

        Returns:
            Any: The subject of the token if verification is successful.

        Raises:
            jwt.ExpiredSignatureError: If the token is expired.
            jwt.InvalidSignatureError: If the signature is invalid.
        """
        payload = jwt.decode(
            token, signing_cookies.SIGNIN_SECRET_KEY, algorithms=jwt_config.JWT_ALGORITHM
        )
        return payload

    def decode_reset_password_token(self, token: str, max_age: int = None):
        """
        This function is used to decode reset tokens

        Args:
            token (str): Encoded token string

        Returns:

            Decoded token information
        """
        # Default token expire time is 24hr (86400 Sec)
        if not max_age:
            max_age = 86400

        try:
            payload = key.loads(token, max_age=max_age)

            return payload
        except SignatureExpired:
            raise SignatureExpired("Your token is expired!")
        except BadSignature:
            raise BadSignature("Your token is invalid")

    def encode_reset_password_link(self, receiver_email: str):
        """
        Generates the reset password link using reset token

        Args:
        receiver_email(str): The email address of user
        holder (bool): Whether a holder user or business user

        Returns:
            reset password link
        """

        try:
            reset_token = key.dumps(
                {
                    "receiver_email": receiver_email,
                    "reset_key": signing_cookies.RESET_KEY,
                }
            )

            return f"{BACKEND_URL}auth/reset/{reset_token}"
        except:
            return StandardResponse(
                status.HTTP_400_BAD_REQUEST, data=None, message="Failed to encode!"
            ).make
