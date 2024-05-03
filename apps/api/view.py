""" View file includes endpoint and websocket"""
import os
from fastapi import status
from fastapi_versioning import version
from websockets.exceptions import ConnectionClosed
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, File, UploadFile
from apps.utils.standard_response import StandardResponse
from apps.utils.wsoc_conn_manager import ConnectionManager
from apps.constant import constant
from config.project_path import MEDIA_ROOT

# Create APIRouter instance
router = APIRouter()

# Create ConnectionManager instance for managing WebSocket connections
manager = ConnectionManager()


@router.post("/div")
@version(2)
async def process_user_input(num1: float, num2: float):
    """
    Sample Endpoint to perform division operation.

    Args:
        num1 (float): The numerator.
        num2 (float): The denominator.

    Returns:
        StandardResponse: Response indicating success or failure with appropriate message.
    """
    try:
        result = num1 / num2
    except ZeroDivisionError as e:
        return StandardResponse(
            False, status.HTTP_400_BAD_REQUEST, "Division by zero is not allowed.", {
                e}
        )
    else:
        return StandardResponse(
            True, status.HTTP_200_OK, "Division successful.", {
                "result": result}
        )


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file.

    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        StandardResponse: Response indicating success or failure with appropriate message.
    """
    try:
        # Save the uploaded file in the backend
        file_path = os.path.join(MEDIA_ROOT, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        return StandardResponse(
            True, status.HTTP_200_OK, "File has been Uploaded Successfully..!", constant.STATUS_SUCCESS
        )
    except Exception as e:
        # Return error response if an exception occurs during file upload
        return StandardResponse(
            False, status.HTTP_500_INTERNAL_SERVER_ERROR, str(
                e), constant.ERROR_MSG
        )


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for handling chat communication.

    Args:
        websocket (WebSocket): WebSocket connection instance.
        user_id (int): User ID associated with the WebSocket connection.
    """
    # Connect the WebSocket
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Receive text message from the WebSocket
            data = await websocket.receive_text()
            if data.lower() == "close":
                await manager.send_ping_message(websocket)
            else:
                print(f'CLIENT says - {data}')
                # Send a personal message to the connected client
                await manager.send_personal_message(
                    f"You wrote: {data}", websocket, user_id
                )
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        print('\n\n  Client disconnected', e)
    except ConnectionClosed as e:
        manager.disconnect(websocket)
        print('\n\n  Client disconnected', e)
