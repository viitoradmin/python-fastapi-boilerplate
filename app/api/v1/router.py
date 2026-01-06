"""
API Version 1 Router.

This module creates and configures the FastAPI app instance for API v1.
"""
import os

from fastapi import FastAPI

from app.api.v1.routes import auth, health, api_keys


def create_app_v1() -> FastAPI:
    """
    Create FastAPI application instance for API v1.
    
    Returns:
        FastAPI: Configured FastAPI app for v1
    """
    env = os.environ.get("ENV", "local")
    
    app_v1 = FastAPI(
        title="EveryCRED DCS API v1",
        description="""\n
        \n## EveryCRED DCS API Version 1\n
        
        \nThis is the first version of the EveryCRED DCS API featuring:\n
        
        \n###  Authentication System\n
        \n- User registration with Argon2 password hashing\n
        \n- Secure user login and authentication\n
        \n- Password security with automatic hash migration\n
        
        \n###  Health Monitoring\n
        \n- System health checks\n
        \n- Service status monitoring\n
        
        \n###  Security Features\n
        \n- Argon2id password hashing (industry standard)\n
        \n- Input validation and sanitization\n
        \n- Security headers middleware\n
        \n- Rate limiting protection\n
        
        \n###  Documentation\n
        \n- Interactive API documentation (Swagger UI)\n
        \n- Alternative documentation (ReDoc)\n
        \n- OpenAPI 3.1.0 specification\n
        """,
        version="1.0.0",
        docs_url="/docs" if env != "prod" else None,
        redoc_url="/redoc" if env != "prod" else None,
    )
    
    # Include route modules
    # Note: No need for /api/v1 prefix here since app is mounted at /api/v1 in server.py
    app_v1.include_router(health.router, tags=["health"])
    app_v1.include_router(auth.router,  tags=["auth"])
    app_v1.include_router(api_keys.router, tags=["Api Keys"])
    
    return app_v1
