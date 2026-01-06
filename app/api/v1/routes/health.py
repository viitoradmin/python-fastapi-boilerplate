"""
Health check routes for API v1.

This module contains health monitoring endpoints.
"""
import os
from datetime import datetime
from fastapi import APIRouter

from app.core.responses import StandardResponse
from app.core.utils import constant_variable

router = APIRouter(prefix="/health")


@router.get("")
async def health_check():
    """
    Health check endpoint for API v1.
    
    Returns:
        StandardResponse: Health status with system information
    """
    env = os.environ.get("ENV", "local")
    
    health_data = {
        "service": "EveryCRED DCS API v1",
        "version": "1.0.0",
        "environment": env,
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "healthy",
        "features": {
            "authentication": "enabled",
            "argon2_hashing": "enabled",
            "security_headers": "enabled",
            "rate_limiting": "enabled"
        }
    }
    
    response = StandardResponse.success(
        data=health_data,
        message=constant_variable.GENERAL_MESSAGES["HEALTH_OK"]
    )
    
    return response.make