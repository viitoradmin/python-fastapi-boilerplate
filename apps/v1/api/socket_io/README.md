# Socket.IO Integration (API module)

Reusable Socket.IO layer for the FastAPI boilerplate, placed under `apps/v1/api/` so it matches the existing project pattern.

## Structure

```
apps/v1/api/socket_io/
├── __init__.py
├── constants.py
├── exceptions.py
├── view.py          # default Socket.IO event handlers (register_default_handlers)
├── schema.py
└── services/
    └── __init__.py
```

Socket.IO server factory (`create_socket_app`, `get_sio`) lives in `apps/server.py`.  
Socket.IO auth middleware lives in `middleware/socket_auth_middleware.py` (project root).

Config lives in `config/socket_config.py`.

## How this boilerplate works

- `apps/server.py` creates the **Socket.IO server** and wraps the FastAPI app:
  - `create_socket_app(fastapi_app)` → combined ASGI app
  - `get_sio()` → global `AsyncServer` instance (use it anywhere to emit)
- `socket_io/view.py` contains default **host/server event handlers**:
  - `connect`, `disconnect`, `error`, `join_room`, `leave_room`, `message`
- `middleware/socket_auth_middleware.py` (project root) is a hook for **handshake auth** (validate token, etc.).

> The “host events” are the Python handlers you define on `sio` (what your backend listens to and emits).  
> The “client events” are what your frontend/mobile app emits or listens to through Socket.IO JS.

## Using host/server events

### 1. Define host handlers (what server listens to)

Add handlers in `socket_io/view.py` (or add modules under `socket_io/` and import them from there):

```python
from typing import Any

def register_default_handlers(sio):
    @sio.event
    async def my_custom_event(sid: str, data: dict | Any) -> None:
        # handle client->server event
        # e.g. persist to DB, then reply
        await sio.emit("my_custom_event_ack", {"ok": True}, to=sid)
```

### 2. Emit from HTTP routes / services / background tasks

Anywhere in your FastAPI code (e.g. in a service or API view):

```python
from apps.server import get_sio

async def notify_user(user_id: int, payload: dict) -> None:
    sio = get_sio()
    room = f"user:{user_id}"
    await sio.emit("user_notification", payload, room=room)
```

This is how you implement **host events** (server pushing events to clients).

## Using client events

Client (browser / mobile / other service) connects and uses `emit` / `on`:

```javascript
import { io } from "socket.io-client";

const socket = io("http://localhost:8000", {
  path: "/socket.io",
  auth: { token: "optional-jwt" }
});

socket.on("connect", () => console.log("connected", socket.id));

// client -> host (server listens with @sio.event)
socket.emit("my_custom_event", { foo: "bar" });

// join a room so host can broadcast
socket.emit("join_room", { room: "user:123" });

// listen to host events
socket.on("user_notification", (data) => {
  console.log("Got notification from host:", data);
});
```

## Summary

- **Host/server events**: define handlers in `socket_io/view.py` (or sibling modules) and emit with `get_sio().emit(...)`.
- **Client events**: frontend/mobile uses Socket.IO JS `emit`/`on` to talk to those handlers.

