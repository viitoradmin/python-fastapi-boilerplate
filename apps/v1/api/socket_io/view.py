"""This module is responsible to contain API's endpoint (Socket.IO helpers)."""

import logging
from typing import Any

from fastapi import APIRouter, status

from apps.v1.api.socket_io.exceptions import SocketAuthError
from core.utils.standard_response import StandardResponse

logger = logging.getLogger(__name__)

router = APIRouter()


def register_default_handlers(sio: Any) -> None:
    """
    Register default namespace (/) event handlers on the given AsyncServer.
    Call this once after creating the server.
    """

    @sio.event
    async def connect(sid: str, environ: dict, auth: dict | None) -> bool | None:
        """
        Fired when a client connects. Return False or raise to reject.
        Use auth from client: io.connect(url, { auth: { token: '...' } }).
        """
        logger.info("Socket connect sid=%s auth=%s", sid, auth)
        # Optional: validate auth and reject if invalid
        # if not _validate_auth(auth):
        #     raise SocketAuthError("Invalid token")
        return True

    @sio.event
    async def disconnect(sid: str) -> None:
        """Fired when client disconnects (or connection is lost)."""
        logger.info("Socket disconnect sid=%s", sid)

    @sio.event
    async def error(sid: str, data: Any) -> None:
        """Fired when client sends an error event (or server emits one)."""
        logger.warning("Socket error sid=%s data=%s", sid, data)

    @sio.event
    async def join_room(sid: str, data: dict | str) -> None:
        """
        Client sends { "room": "room_name" } or "room_name" to join.
        Enables broadcast to that room via sio.emit(..., room=room_name).
        """
        room = data.get("room", data) if isinstance(data, dict) else data
        if not room or not isinstance(room, str):
            await sio.emit("error", {"message": "room required"}, to=sid)
            return
        await sio.enter_room(sid, room)
        await sio.emit("joined_room", {"room": room}, to=sid)
        logger.debug("sid=%s joined room=%s", sid, room)

    @sio.event
    async def leave_room(sid: str, data: dict | str) -> None:
        """Client sends { "room": "room_name" } or "room_name" to leave."""
        room = data.get("room", data) if isinstance(data, dict) else data
        if not room or not isinstance(room, str):
            return
        await sio.leave_room(sid, room)
        await sio.emit("left_room", {"room": room}, to=sid)
        logger.debug("sid=%s left room=%s", sid, room)

    @sio.event
    async def message(sid: str, data: Any) -> None:
        """
        Generic message event. Echo or broadcast as needed.
        Example: emit to sender only; extend to broadcast to room.
        """
        await sio.emit("message", {"echo": data, "from": sid}, to=sid)


class SocketIOApi:
    """Versioned endpoints related to Socket.IO (optional)."""

    @router.get("/socket-io/health")
    async def socket_io_health():
        return StandardResponse(True, status.HTTP_200_OK, {"ok": True}, "OK").make

