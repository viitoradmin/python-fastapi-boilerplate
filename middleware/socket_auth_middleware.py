"""
Optional Socket.IO connection auth middleware.

Client can pass auth in handshake: io.connect(url, { auth: { token: "..." } }).
Validate here and raise SocketAuthError to reject the connection.
"""

import logging

from apps.v1.api.socket_io.exceptions import SocketAuthError

logger = logging.getLogger(__name__)


async def socket_auth_middleware(
    sid: str, environ: dict, auth: dict | None
) -> dict | None:
    """
    Validate handshake auth. Return auth (or modified) to accept; raise to reject.
    Override or replace this in your project (e.g. verify JWT from auth.get("token")).
    """
    if auth is None:
        auth = {}
    # Example: require token in production (disabled by default)
    # token = (auth or {}).get("token")
    # if not token or not await verify_token(token):
    #     raise SocketAuthError("Invalid or missing token")
    return auth
