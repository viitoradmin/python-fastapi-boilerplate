from fastapi import APIRouter
from app.services.llm_service import generate_text 
router = APIRouter(tags=["inference"])


@router.get("/")
async def hello_world():
    return "Hello, From FastAPI!"

@router.post("/chat")
async def chat(user_input: str):
    # TODO: Complete the functionality here
    pass
