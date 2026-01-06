"""
This module provides a standard response format for API responses.
"""

from typing import Optional, Union, Any
from fastapi.responses import JSONResponse

from app.core.utils import constant_variable


class StandardResponse:
    """
    Universal class to return standard API responses.

    This class provides a consistent response format across all API endpoints
    with proper status handling, data formatting, and cookie management.

    Attributes:
        status (str): The response status (success/fail/error)
        status_code (int): The HTTP status code
        data (Optional[Union[dict, list, Any]]): The response data
        message (str): The response message
        cookies (dict): Cookies to set in the response
    """

    def __init__(
        self,
        status_code: int,
        data: Optional[Union[dict, list, Any]] = None,
        message: str = "",
        cookies: Optional[dict] = None,
    ) -> None:
        """
        Initialize the standard response.

        Args:
            status_code (int): The HTTP status code
            data (Optional[Union[dict, list, Any]]): The response data
            message (str): The response message
            cookies (Optional[dict]): Cookies to set in the response

        Returns:
            None
        """
        self.status_code = status_code
        self.data = data
        self.message = message
        self.cookies = cookies or {}
        
        # Determine status based on status code
        self.status = self._determine_status(status_code)

    def _determine_status(self, status_code: int) -> str:
        """
        Determine the response status based on HTTP status code.

        Args:
            status_code (int): The HTTP status code

        Returns:
            str: The response status (success/fail/error)
        """
        if status_code in constant_variable.SUCCESS_STATUS_CODES:
            return constant_variable.STATUS_SUCCESS
        elif 400 <= status_code < 500:
            return constant_variable.STATUS_FAIL
        else:
            return constant_variable.STATUS_ERROR

    @property
    def make(self) -> JSONResponse:
        """
        Generate the JSON response with standard format.

        Returns:
            JSONResponse: The formatted JSON response
        """
        content = {
            "status": self.status,
            "data": self.data,
            "message": self.message
        }
        
        response = JSONResponse(
            content=content,
            status_code=self.status_code
        )

        # Set cookies if provided
        for key, value in self.cookies.items():
            response.set_cookie(
                key=key,
                value=value,
                httponly=constant_variable.COOKIE_SETTINGS["HTTPONLY"],
                secure=constant_variable.COOKIE_SETTINGS["SECURE"],
                samesite=constant_variable.COOKIE_SETTINGS["SAMESITE"],
                max_age=constant_variable.COOKIE_SETTINGS["MAX_AGE"],
            )

        return response

    @classmethod
    def success(
        cls,
        data: Optional[Union[dict, list, Any]] = None,
        message: str = "Operation successful",
        status_code: int = constant_variable.HTTP_200_OK,
        cookies: Optional[dict] = None,
    ) -> "StandardResponse":
        """
        Create a success response.

        Args:
            data: The response data
            message: Success message
            status_code: HTTP status code (default: 200)
            cookies: Cookies to set

        Returns:
            StandardResponse: Success response instance
        """
        return cls(
            status_code=status_code,
            data=data,
            message=message,
            cookies=cookies
        )

    @classmethod
    def created(
        cls,
        data: Optional[Union[dict, list, Any]] = None,
        message: str = "Resource created successfully",
        cookies: Optional[dict] = None,
    ) -> "StandardResponse":
        """
        Create a 201 Created response.

        Args:
            data: The response data
            message: Success message
            cookies: Cookies to set

        Returns:
            StandardResponse: Created response instance
        """
        return cls(
            status_code=constant_variable.HTTP_201_CREATED,
            data=data,
            message=message,
            cookies=cookies
        )

    @classmethod
    def bad_request(
        cls,
        message: str = "Bad request",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 400 Bad Request response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Bad request response instance
        """
        return cls(
            status_code=constant_variable.HTTP_400_BAD_REQUEST,
            data=data,
            message=message
        )

    @classmethod
    def unauthorized(
        cls,
        message: str = "Unauthorized access",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 401 Unauthorized response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Unauthorized response instance
        """
        return cls(
            status_code=constant_variable.HTTP_401_UNAUTHORIZED,
            data=data,
            message=message
        )

    @classmethod
    def forbidden(
        cls,
        message: str = "Access forbidden",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 403 Forbidden response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Forbidden response instance
        """
        return cls(
            status_code=constant_variable.HTTP_403_FORBIDDEN,
            data=data,
            message=message
        )

    @classmethod
    def not_found(
        cls,
        message: str = "Resource not found",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 404 Not Found response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Not found response instance
        """
        return cls(
            status_code=constant_variable.HTTP_404_NOT_FOUND,
            data=data,
            message=message
        )

    @classmethod
    def conflict(
        cls,
        message: str = "Resource conflict",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 409 Conflict response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Conflict response instance
        """
        return cls(
            status_code=constant_variable.HTTP_409_CONFLICT,
            data=data,
            message=message
        )

    @classmethod
    def validation_error(
        cls,
        message: str = "Validation failed",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 422 Unprocessable Entity response.

        Args:
            message: Error message
            data: Validation error details

        Returns:
            StandardResponse: Validation error response instance
        """
        return cls(
            status_code=constant_variable.HTTP_422_UNPROCESSABLE_ENTITY,
            data=data,
            message=message
        )

    @classmethod
    def internal_error(
        cls,
        message: str = "Internal server error",
        data: Optional[Union[dict, list, Any]] = None,
    ) -> "StandardResponse":
        """
        Create a 500 Internal Server Error response.

        Args:
            message: Error message
            data: Additional error data

        Returns:
            StandardResponse: Internal error response instance
        """
        return cls(
            status_code=constant_variable.HTTP_500_INTERNAL_SERVER_ERROR,
            data=data,
            message=message
        )