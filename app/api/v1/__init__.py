from fastapi import APIRouter

from .inference import router as inference_router
from ...core.config import settings

router = APIRouter(prefix=settings.API_VERSION)
router.include_router(inference_router)