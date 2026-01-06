"""
API Version 2 Router.

This module creates and configures the FastAPI app instance for API v2.
"""
import os

from fastapi import FastAPI, APIRouter

from app.api.v2.routes import health, api_keys


def create_app_v2() -> FastAPI:
    """
    Create FastAPI application instance for API v2.
    
    Returns:
        FastAPI: Configured FastAPI app for v2
    """
    env = os.environ.get("ENV", "local")
    
    app_v2 = FastAPI(
        title="EveryCRED DCS API v2",
        description="""
        ## EveryCRED DCS API Version 2
        
        This is the enhanced version of the EveryCRED DCS API featuring:
        
        ### 🚀 Enhanced Features
        - Improved performance and scalability
        - Advanced authentication mechanisms
        - Enhanced security protocols
        
        ### 🏥 Health Monitoring
        - Advanced system health checks
        - Detailed service metrics
        - Performance monitoring
        
        ### 🔮 Future Features (Coming Soon)
        - Advanced user management
        - Enhanced data processing
        - Real-time notifications
        - Advanced analytics
        
        ### 📚 Documentation
        - Interactive API documentation (Swagger UI)
        - Alternative documentation (ReDoc)
        - OpenAPI 3.1.0 specification
        
        > **Note**: This version is under active development. 
        > For production use, consider using API v1.
        """,
        version="2.0.0",
        docs_url="/docs" if env != "prod" else None,
        redoc_url="/redoc" if env != "prod" else None,
    )
    
    # Create routers with prefixes
    v2_router = APIRouter()
    
    # Include route modules
    v2_router.include_router(health.router, tags=["health"])
    v2_router.include_router(api_keys.router, tags=["Api keys v2"])
    
    # Include the main router (no prefix needed as app is mounted at /api/v2)
    app_v2.include_router(v2_router)
    
    return app_v2
