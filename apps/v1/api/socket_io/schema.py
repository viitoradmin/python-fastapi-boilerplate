"""This module is for swagger and request parameter schema (Socket.IO)."""

from pydantic import BaseModel


class JoinRoomPayload(BaseModel):
    room: str


class LeaveRoomPayload(BaseModel):
    room: str

