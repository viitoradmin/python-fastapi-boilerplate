""" This is file is websocket connect manager, useful to handle events of wbesoket of fastapi"""
import json
from fastapi import WebSocket
from apps.ml_backend.inference import ml_inference


class ConnectionManager():
    """Class managing WebSocket connections."""

    def __init__(self):
        """Initialize the ConnectionManager."""
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a WebSocket."""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.user_id = user_id
        except Exception as e:
            print(f"Error in connecting WebSocket: {e}")

    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket."""
        self.active_connections.remove(websocket)

    async def send_personal_message(
        self, message: str, websocket: WebSocket, user_id: int
    ):
        """Send a personal message to a WebSocket."""
        # if user_id != self.user_id():
        #     self.create_history()

        # run the inference model on latest user-input
        inf_response = ml_inference(message)
        # to send the json over websocket to client
        await websocket.send_text(json.dumps(inf_response))

    async def send_close_message(self, websocket: WebSocket):
        """Send a close message to a WebSocket."""
        await websocket.send_text("connection closed")

    async def send_ping_message(self, websocket: WebSocket):
        """Send a ping message to a WebSocket."""
        # useful to send ping messgae to client if client got disconnected
        await websocket.send_text("ping")
