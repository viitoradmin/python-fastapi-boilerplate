"""
Socket.IO–specific exceptions.

Use in handlers to reject connections or signal errors; can be mapped
to disconnect or error events for the client.
"""


class SocketIOError(Exception):
    """Base for Socket.IO errors."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or "socket_error"
        super().__init__(self.message)


class SocketAuthError(SocketIOError):
    """Raised when handshake auth is invalid."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class SocketForbiddenError(SocketIOError):
    """Raised when connection or action is not allowed."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, code="forbidden")
