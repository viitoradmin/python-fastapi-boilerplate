"""
Socket.IO server configuration.

Centralizes all Socket.IO-related settings so the same structure
can be reused across projects. Uses env vars with sensible defaults.
"""
import os
from typing import Any

# Mount path for Socket.IO engine (client connects to this path)
SOCKETIO_PATH = os.getenv("SOCKETIO_PATH", "socket.io")

# CORS: comma-separated origins, or "*" for allow all
SOCKETIO_CORS_ALLOWED_ORIGINS = os.getenv("SOCKETIO_CORS_ALLOWED_ORIGINS", "*")

# Engine.IO / connection tuning
SOCKETIO_PING_TIMEOUT = int(os.getenv("SOCKETIO_PING_TIMEOUT", "60"))
SOCKETIO_PING_INTERVAL = int(os.getenv("SOCKETIO_PING_INTERVAL", "25"))
SOCKETIO_MAX_HTTP_BUFFER_SIZE = int(os.getenv("SOCKETIO_MAX_HTTP_BUFFER_SIZE", "1000000"))

# Redis: when set, use Redis manager for multi-worker / multi-instance scaling
# Format: redis://host:port/db or redis://:password@host:port/db
SOCKET_REDIS_URL = os.getenv("SOCKET_REDIS_URL", "")

# Namespace to use as default (empty string = default namespace)
DEFAULT_NAMESPACE = "/"


def get_socketio_cors_origins() -> list[str] | str:
    """Return CORS origins for Socket.IO. '*' means allow all."""
    raw = (SOCKETIO_CORS_ALLOWED_ORIGINS or "").strip()
    if not raw or raw == "*":
        return "*"
    return [o.strip() for o in raw.split(",") if o.strip()]


def get_socketio_server_kwargs() -> dict[str, Any]:
    """Kwargs for AsyncServer constructor. Used by socket_io.server."""
    kwargs: dict[str, Any] = {
        "async_mode": "asgi",
        "cors_allowed_origins": get_socketio_cors_origins(),
        "ping_timeout": SOCKETIO_PING_TIMEOUT,
        "ping_interval": SOCKETIO_PING_INTERVAL,
        "max_http_buffer_size": SOCKETIO_MAX_HTTP_BUFFER_SIZE,
        "logger": False,
        "engineio_logger": False,
    }
    if SOCKET_REDIS_URL:
        # Lazy import so redis is optional at import time
        try:
            from socketio import AsyncRedisManager
            kwargs["client_manager"] = AsyncRedisManager(SOCKET_REDIS_URL)
        except ImportError:
            pass
    return kwargs
