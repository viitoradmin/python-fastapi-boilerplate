"""
HTTP Security Headers Middleware Module.

This module provides middleware components for adding security-related HTTP headers
to FastAPI application responses. The primary focus is on implementing HTTP Strict
Transport Security (HSTS) to enforce secure connections and protect against
protocol downgrade attacks and cookie hijacking.

The HSTSMiddleware class automatically adds the Strict-Transport-Security header
to all HTTP responses, instructing browsers to only connect to the server over
HTTPS for a specified duration. This is a critical security measure for web
applications that handle sensitive data or require secure communication.

Note:
    HSTS should only be enabled in production environments with valid SSL/TLS
    certificates. Enabling HSTS in development can cause issues if the application
    is accessed over HTTP or with self-signed certificates.
"""

from collections import OrderedDict

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable


CSP: dict[str, str | list[str]] = {
    "default-src": "'self'",
    "img-src": [
        "*",
        # For SWAGGER UI
        "data:",
    ],
    "connect-src": ["'self'", "https://cdn.jsdelivr.net"],
    "script-src": ["'self'", "https://cdn.jsdelivr.net", "'unsafe-inline'"],
    "style-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    "script-src-elem": [
        # For SWAGGER UI
        "'self'",
        "https://cdn.jsdelivr.net",
        "'unsafe-inline'",
    ],
    "style-src-elem": [
        # For SWAGGER UI
        "'self'",
        "https://cdn.jsdelivr.net",
        "'unsafe-inline'",
    ],
}

def parse_policy(policy: dict[str, str | list[str]] | str) -> str:
    """Parse a given policy dict to string."""
    if isinstance(policy, str):
        # parse the string into a policy dict
        policy_string = policy
        policy = OrderedDict()

        for policy_part in policy_string.split(";"):
            policy_parts = policy_part.strip().split(" ")
            policy[policy_parts[0]] = " ".join(policy_parts[1:])

    policies = []
    for section, content in policy.items():
        if not isinstance(content, str):
            content = " ".join(content)
        policy_part = f"{section} {content}"

        policies.append(policy_part)

    parsed_policy = "; ".join(policies)

    return parsed_policy

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    def __init__(self, app: FastAPI, csp: bool = True) -> None:
        """Init SecurityHeadersMiddleware.

        :param app: FastAPI instance
        :param no_csp: If no CSP should be used;
            defaults to :py:obj:`False`
        """
        super().__init__(app)
        self.csp = csp

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        """Dispatch of the middleware.

        :param request: Incoming request
        :param call_next: Function to process the request
        :return: Return response coming from from processed request
        """
        headers = {
            "Content-Security-Policy": "" if not self.csp else parse_policy(CSP),
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31556926; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
        }
        response = await call_next(request)
        response.headers.update(headers)

        return response