"""This module contains application routes."""
from fastapi import APIRouter
from app.services.llm_service import generate_text
router = APIRouter(tags=["inference"])


@router.get("/")
async def hello_world():
    """This endpoint will return string.

    Returns:
        str: String representation of the message.
    """
    return "Hello, From FastAPI!"

@router.post("/chat")
async def chat(user_input: str):
    """This endpoint will return generated text from user input.

    Args:
        user_input (str): Input string provided by user.

    Returns:
        _type_: Generated text
    """
    return generate_text(user_input=user_input)

