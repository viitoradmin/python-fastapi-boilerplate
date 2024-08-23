"""This module contains API routes for interacting with application."""

from fastapi import APIRouter

from app.api.v1.inference import router as inference_router
from app.core.config import settings

router = APIRouter(prefix=settings.API_VERSION)
router.include_router(inference_router)
