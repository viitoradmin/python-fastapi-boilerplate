"""
Socket.IO event and room constants.

Use these across handlers and clients for consistency. Projects can extend
with their own event names and room prefixes.
"""

# Built-in / reserved (Socket.IO / Engine.IO)
EVENT_CONNECT = "connect"
EVENT_DISCONNECT = "disconnect"
EVENT_ERROR = "error"

# Common custom events (optional; use as needed)
EVENT_MESSAGE = "message"
EVENT_JOIN_ROOM = "join_room"
EVENT_LEAVE_ROOM = "leave_room"
EVENT_PING = "ping"
EVENT_PONG = "pong"
EVENT_BROADCAST = "broadcast"

# Room name prefixes (avoids collisions between features)
ROOM_PREFIX_USER = "user:"
ROOM_PREFIX_CHANNEL = "channel:"
ROOM_PREFIX_SESSION = "session:"

# Default namespace
NAMESPACE_DEFAULT = "/"
