"""
Global error handling middleware.

This module provides comprehensive error handling for the FastAPI application.
"""

import logging
from typing import Any
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.responses import StandardResponse
from app.core.utils import constant_variable

# Configure logger
logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    
    Catches and formats all unhandled exceptions into standard response format.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and handle any exceptions.

        Args:
            request: The incoming request
            call_next: The next middleware or endpoint

        Returns:
            Response: The response with proper error handling
        """
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Handle FastAPI HTTP exceptions
            return await self._handle_http_exception(request, exc)
        except RequestValidationError as exc:
            # Handle Pydantic validation errors
            return await self._handle_validation_error(request, exc)
        except Exception as exc:
            # Handle all other unexpected exceptions
            return await self._handle_general_exception(request, exc)

    async def _handle_http_exception(
        self, 
        request: Request, 
        exc: HTTPException
    ) -> Response:
        """
        Handle FastAPI HTTP exceptions.

        Args:
            request: The incoming request
            exc: The HTTP exception

        Returns:
            Response: Formatted error response
        """
        logger.warning(
            f"HTTP Exception: {exc.status_code} - {exc.detail} "
            f"Path: {request.url.path} Method: {request.method}"
        )

        # Extract message from detail (handle both string and dict formats)
        message = exc.detail
        if isinstance(exc.detail, dict):
            message = exc.detail.get("message", str(exc.detail))

        response = StandardResponse(
            status_code=exc.status_code,
            message=str(message),
            data=None
        )
        
        return response.make

    async def _handle_validation_error(
        self, 
        request: Request, 
        exc: RequestValidationError
    ) -> Response:
        """
        Handle Pydantic validation errors.

        Args:
            request: The incoming request
            exc: The validation error

        Returns:
            Response: Formatted validation error response
        """
        logger.warning(
            f"Validation Error: {len(exc.errors())} errors "
            f"Path: {request.url.path} Method: {request.method}"
        )

        # Format validation errors
        formatted_errors = []
        for error in exc.errors():
            formatted_errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })

        response = StandardResponse(
            status_code=constant_variable.HTTP_422_UNPROCESSABLE_ENTITY,
            message=constant_variable.GENERAL_MESSAGES["VALIDATION_ERROR"],
            data={"errors": formatted_errors}
        )
        
        return response.make

    async def _handle_general_exception(
        self, 
        request: Request, 
        exc: Exception
    ) -> Response:
        """
        Handle all other unexpected exceptions.

        Args:
            request: The incoming request
            exc: The exception

        Returns:
            Response: Formatted internal error response
        """
        logger.error(
            f"Unhandled Exception: {type(exc).__name__}: {str(exc)} "
            f"Path: {request.url.path} Method: {request.method}",
            exc_info=True
        )

        response = StandardResponse(
            status_code=constant_variable.HTTP_500_INTERNAL_SERVER_ERROR,
            message=constant_variable.GENERAL_MESSAGES["INTERNAL_ERROR"],
            data=None
        )
        
        return response.make


def setup_error_handlers(app) -> None:
    """
    Setup global error handlers for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.warning(
            f"HTTP Exception: {exc.status_code} - {exc.detail} "
            f"Path: {request.url.path}"
        )

        message = exc.detail
        if isinstance(exc.detail, dict):
            message = exc.detail.get("message", str(exc.detail))

        response = StandardResponse(
            status_code=exc.status_code,
            message=str(message)
        )
        
        return response.make

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        logger.warning(
            f"Validation Error: {len(exc.errors())} errors "
            f"Path: {request.url.path}"
        )

        formatted_errors = []
        for error in exc.errors():
            formatted_errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })

        response = StandardResponse(
            status_code=constant_variable.HTTP_422_UNPROCESSABLE_ENTITY,
            message=constant_variable.GENERAL_MESSAGES["VALIDATION_ERROR"],
            data={"errors": formatted_errors}
        )
        
        return response.make

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(
            f"Unhandled Exception: {type(exc).__name__}: {str(exc)} "
            f"Path: {request.url.path}",
            exc_info=True
        )

        response = StandardResponse(
            status_code=constant_variable.HTTP_500_INTERNAL_SERVER_ERROR,
            message=constant_variable.GENERAL_MESSAGES["INTERNAL_ERROR"]
        )
        
        return response.make