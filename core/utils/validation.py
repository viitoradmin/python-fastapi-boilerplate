import base64
import imghdr
from math import cos
import mimetypes
import re
from datetime import datetime
from urllib.parse import urlparse

import bleach

from core.utils import constant_variable


class ValidationMethods:
    def not_null_validator(self, v, field):
        if v == [] or v == {} or v == "":
            raise ValueError(f"{field} must be required")
        return v

    def check_number_validator(self, v, field):
        if v == str(v):
            raise ValueError(f"{field} must be an integer")
        return v

    def validate_password(self, value):

        # Check length
        if len(value) <= 7:
            raise ValueError("Admin password must be at least 8 characters long")

        # Check for lowercase letter
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        # Check for uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        # Check for digit
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"|,.<>/?]', value):
            raise ValueError("Password must contain at least one special character")

        return value

    def sanitize_value(self, values):
        """Sanitize input values by removing HTML tags.

        Args:
            values (str): The input values to be sanitized.

        Returns:
            str: The sanitized input values.

        """
        if values:
            return bleach.clean(
                values, tags={}, attributes=[], strip=constant_variable.STATUS_TRUE
            )

    def validate_number(
        self,
        fvalue,
        num_type=constant_variable.STATUS_NULL,
        min_value=constant_variable.STATUS_NULL,
        max_value=constant_variable.STATUS_NULL,
    ):
        # If not mandatory and the field value is empty or constant_variable.STATUS_NULL, it's valid
        if fvalue:
            try:
                # Convert the value to float or int based on the type specified (num_type)
                if num_type == "int":
                    number = int(fvalue)
                elif num_type == "float":
                    number = float(fvalue)
                else:
                    # Default to trying to convert to float first
                    number = float(fvalue)
                    if number.is_integer():
                        number = int(
                            number
                        )  # Convert to int if it's an integer-like float

                # Check if the number is within the specified range
                if (
                    min_value is not None
                    and number < min_value
                ):
                    return constant_variable.STATUS_FALSE
                if (
                    max_value is not None
                    and number > max_value
                ):
                    return constant_variable.STATUS_FALSE

                return (
                    constant_variable.STATUS_TRUE
                )  # Number is valid if all checks pass

            except (ValueError, TypeError):
                # If conversion fails or an invalid type is provided
                return constant_variable.STATUS_FALSE
        return constant_variable.STATUS_TRUE

    def validate_date(self, fvalue):
        if fvalue:
            try:
                # Expected format for date: YYYY-MM-DD
                datetime.strptime(fvalue, "%Y-%m-%d")
                return constant_variable.STATUS_TRUE
            except ValueError:
                return constant_variable.STATUS_FALSE
        return constant_variable.STATUS_TRUE

    def validate_datetime(self, is_mandatory, fvalue):
        if not is_mandatory and fvalue in [constant_variable.STATUS_NULL, "", ""]:
            return constant_variable.STATUS_TRUE

        try:
            # Expected format for datetime: YYYY-MM-DDTHH:MM:SS+HH:MM
            datetime.fromisoformat(fvalue)
            return constant_variable.STATUS_TRUE
        except ValueError:
            return constant_variable.STATUS_FALSE

    def validate_boolean(self, is_mandatory, fvalue):
        if not is_mandatory and fvalue in [constant_variable.STATUS_NULL, "", ""]:
            return constant_variable.STATUS_TRUE

        # Check for boolean values in different formats
        if isinstance(fvalue, bool):
            return constant_variable.STATUS_TRUE
        if isinstance(fvalue, str):
            lower_value = fvalue.lower()
            if lower_value in ["true", "false", "1", "0"]:
                return constant_variable.STATUS_TRUE
        return constant_variable.STATUS_FALSE

    def validate_url(self, is_mandatory, fvalue):
        if not is_mandatory and fvalue in [constant_variable.STATUS_NULL, "", ""]:
            return constant_variable.STATUS_TRUE

        try:
            result = urlparse(fvalue)
            return all(
                [result.scheme, result.netloc]
            )  # Ensure URL has scheme and netloc
        except ValueError:
            return constant_variable.STATUS_FALSE

    def validate_file_type(
        self, fvalue, allowed_mime_types=[]
    ):
        if fvalue:
            # Ensure allowed_mime_types is provided; if not, use a default list
            if allowed_mime_types is constant_variable.STATUS_NULL:
                allowed_mime_types = [
                    constant_variable.FILE_TYPE_PDF,
                    constant_variable.FILE_TYPE_IMAGE_PNG,
                    constant_variable.FILE_TYPE_IMAGE_JPEG,
                    constant_variable.FILE_TYPE_EXCEL,
                    constant_variable.FILE_TYPE_MP4,
                    constant_variable.FILE_TYPE_MPEG,
                ]

            try:
                # Decode the Base64 file content
                file_data = base64.b64decode(fvalue)

                # Detect file MIME type (method 1: using imghdr for images)
                mime_type = imghdr.what(constant_variable.STATUS_NULL, file_data)
                if mime_type:  # If imghdr can detect it as an image, append 'image/'
                    mime_type = f"image/{mime_type}"
                else:
                    # Detect MIME type (method 2: using mimetypes)
                    mime_type = mimetypes.guess_type(fvalue)[0]

                # Validate the detected MIME type against the allowed list
                if mime_type in allowed_mime_types:
                    return constant_variable.STATUS_TRUE
                else:
                    return constant_variable.STATUS_FALSE
            except ValueError:
                # If there's an error in decoding Base64 or invalid file content
                return constant_variable.STATUS_FALSE
        return constant_variable.STATUS_TRUE
