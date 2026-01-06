import os
import time
from pathlib import Path
from typing import List

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import Any

from app.api.v1.router import create_app_v1
from app.api.v2.router import create_app_v2
from app.core.middleware.headers import SecurityHeadersMiddleware
from app.core.middleware.error_handler import setup_error_handlers, ErrorHandlerMiddleware
from app.core.responses import StandardResponse


def custom_openapi(app: FastAPI):
    """
    Customize OpenAPI schema with logo and proper metadata.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        dict: OpenAPI schema dictionary
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.1.0",
        description=app.description,
        servers=app.servers,
        routes=app.routes,
    )
    
    # Add custom logo
    openapi_schema["info"]["x-logo"] = {
        "url": "https://img.lovepik.com/element/45015/3146.png_300.png"
    }
    
    app.openapi_schema = openapi_schema
    return openapi_schema


def init_listeners(app_: FastAPI) -> None:
    """
    Initialize exception handlers and listeners for the FastAPI application.
    
    Args:
        app_: FastAPI application instance
    """
    # Pydantic Validation Error Handler
    @app_.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        formatted_errors = []
        for err in exc.errors():
            formatted_errors.append(
                {
                    "field": " -> ".join(
                        str(loc) for loc in err["loc"]
                    ),
                    "message": err["msg"],
                    "type": err["type"],
                }
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "data": None,
                "message": "Validation failed!",
                "errors": formatted_errors,
            },
        )


def make_middleware() -> List[Middleware]:
    """
    Create middleware list for the FastAPI application.
    
    Returns:
        List[Middleware]: List of middleware instances
    """
    env = os.environ.get("ENV", "local")
    enable_csp = env == "prod"
    
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            SecurityHeadersMiddleware, csp=enable_csp
        ),
        Middleware(
            ErrorHandlerMiddleware
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    """
    Create main FastAPI application.
    
    This function creates the main FastAPI application and mounts
    version-specific apps (v1, v2) to it.
    
    Returns:
        FastAPI: The created FastAPI application
    """
    env = os.environ.get("ENV", "local")
    
    app_ = FastAPI(
        title="EveryCRED DCS API Gateway",
        description="""
        The upgraded version of EveryCRED with versioned APIs.
        
        ## Available API Versions:
        
        ### API v1 Documentation:
        - **Swagger UI**: [/api/v1/docs](/api/v1/docs)
        - **ReDoc**: [/api/v1/redoc](/api/v1/redoc)
        - **OpenAPI Schema**: [/api/v1/openapi.json](/api/v1/openapi.json)
        
        ### API v2 Documentation:
        - **Swagger UI**: [/api/v2/docs](/api/v2/docs)
        - **ReDoc**: [/api/v2/redoc](/api/v2/redoc)
        - **OpenAPI Schema**: [/api/v2/openapi.json](/api/v2/openapi.json)
        
        ### Main Gateway:
        - **Health Check**: [/health](/health)
        - **API Status**: [/api/status](/api/status)
        """,
        version="1.0.0",
        docs_url=None if env == "prod" else "/docs",
        redoc_url=None if env == "prod" else "/redoc",
        middleware=make_middleware(),
        swagger_ui_parameters={
            "syntaxHighlight.theme": "obsidian",
            "filter": True,
            "tagsSorter": "alpha",
            "operationsSorter": "alpha",
            "persistAuthorization": True,
            "displayRequestDuration": True,
        },
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True,
        },
    )
    
    # Override OpenAPI schema with custom function
    # app_.openapi = lambda: custom_openapi(app_)
    
    # Initialize listeners and error handlers
    init_listeners(app_=app_)
    setup_error_handlers(app_)
    
    # Create version-specific apps
    app_v1 = create_app_v1()
    app_v2 = create_app_v2()
    
    # Apply custom OpenAPI to version apps
    app_v1.openapi = lambda: custom_openapi(app_v1)
    app_v2.openapi = lambda: custom_openapi(app_v2)
    
    # Mount version-specific apps
    app_.mount("/api/v1", app_v1)
    app_.mount("/api/v2", app_v2)
    
    # Add main app routes for API discovery
    @app_.get("/health", tags=["Gateway"])
    async def health_check():
        """Gateway health check endpoint."""
        from datetime import datetime
        from app.core.utils import constant_variable
        
        health_data = {
            "service": "EveryCRED DCS API Gateway",
            "version": "1.0.0",
            "environment": os.environ.get("ENV", "local"),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy",
            "available_apis": [
                {
                    "version": "v1",
                    "status": "production_ready",
                    "docs": "/api/v1/docs",
                    "redoc": "/api/v1/redoc",
                    "openapi": "/api/v1/openapi.json"
                },
                {
                    "version": "v2", 
                    "status": "in_development",
                    "docs": "/api/v2/docs",
                    "redoc": "/api/v2/redoc",
                    "openapi": "/api/v2/openapi.json"
                }
            ]
        }
        
        response = StandardResponse.success(
            data=health_data,
            message=constant_variable.GENERAL_MESSAGES["HEALTH_OK"]
        )
        
        return response.make
    
    @app_.get("/api/status", tags=["Gateway"])
    async def api_status():
        """Get status and documentation links for all API versions."""
        from datetime import datetime
        from app.core.utils import constant_variable
        
        env = os.environ.get("ENV", "local")
        base_url = os.environ.get("BASE_URL", "http://localhost:8008")
        
        status_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "environment": env,
            "gateway": {
                "title": "EveryCRED DCS API Gateway",
                "version": "1.0.0",
                "status": "operational",
                "docs": f"{base_url}/docs" if env != "prod" else None,
                "redoc": f"{base_url}/redoc" if env != "prod" else None
            },
            "apis": {
                "v1": {
                    "title": "EveryCRED DCS API v1",
                    "version": "1.0.0",
                    "status": "production_ready",
                    "description": "Complete authentication system with Argon2 password hashing",
                    "docs": f"{base_url}/api/v1/docs" if env != "prod" else None,
                    "redoc": f"{base_url}/api/v1/redoc" if env != "prod" else None,
                    "openapi": f"{base_url}/api/v1/openapi.json",
                    "endpoints": [
                        "/api/v1/auth/register",
                        "/api/v1/auth/login", 
                        "/api/v1/health"
                    ]
                },
                "v2": {
                    "title": "EveryCRED DCS API v2",
                    "version": "2.0.0",
                    "status": "in_development", 
                    "description": "Enhanced API with advanced features and improved performance",
                    "docs": f"{base_url}/api/v2/docs" if env != "prod" else None,
                    "redoc": f"{base_url}/api/v2/redoc" if env != "prod" else None,
                    "openapi": f"{base_url}/api/v2/openapi.json",
                    "endpoints": [
                        "/api/v2/health"
                    ]
                }
            }
        }
        
        response = StandardResponse.success(
            data=status_data,
            message="API status retrieved successfully"
        )
        
        return response.make
    
    @app_.get("/", response_class=HTMLResponse, tags=["Gateway"])
    async def api_documentation_hub():
        """API Documentation Hub - Landing page with links to all documentation."""
        env = os.environ.get("ENV", "local")
        
        if env == "prod":
            # In production, just return a simple JSON response
            return JSONResponse({
                "service": "EveryCRED DCS API Gateway",
                "version": "1.0.0",
                "status": "running"
            })
        
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>EveryCRED DCS API Documentation Hub</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #333;
                    position: relative;
                }
                body::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
                                radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
                    pointer-events: none;
                }
                .container { 
                    background: rgba(255, 255, 255, 0.98);
                    backdrop-filter: blur(10px);
                    padding: 3rem;
                    border-radius: 24px;
                    box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.1);
                    max-width: 900px;
                    width: 90%;
                    position: relative;
                    z-index: 1;
                }
                h1 { 
                    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #10b981 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 0.5rem;
                    font-size: 2.8rem;
                    text-align: center;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                }
                .subtitle {
                    text-align: center;
                    color: #64748b;
                    margin-bottom: 3rem;
                    font-size: 1.2rem;
                    font-weight: 500;
                }
                .api-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 2rem;
                    margin-bottom: 2rem;
                }
                .api-card {
                    border: 2px solid #e2e8f0;
                    border-radius: 16px;
                    padding: 2rem;
                    transition: all 0.3s ease;
                    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                    position: relative;
                    overflow: hidden;
                }
                .api-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, #3b82f6, #10b981);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                .api-card:hover::before {
                    opacity: 1;
                }
                .api-card:hover {
                    border-color: #3b82f6;
                    transform: translateY(-8px);
                    box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
                }
                .api-title {
                    font-size: 1.6rem;
                    font-weight: 700;
                    color: #1e293b;
                    margin-bottom: 0.75rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .api-description {
                    color: #64748b;
                    margin-bottom: 1.5rem;
                    line-height: 1.6;
                    font-size: 0.95rem;
                }
                .doc-links {
                    display: flex;
                    gap: 0.75rem;
                    flex-wrap: wrap;
                }
                .doc-link {
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.75rem 1.25rem;
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    font-size: 0.9rem;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                }
                .doc-link:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
                }
                .doc-link.redoc {
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                }
                .doc-link.redoc:hover {
                    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
                }
                .doc-link.openapi {
                    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
                }
                .doc-link.openapi:hover {
                    box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4);
                }
                .gateway-info {
                    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
                    border: 1px solid #cbd5e1;
                    border-radius: 16px;
                    padding: 2rem;
                    margin-top: 2rem;
                    text-align: center;
                }
                .gateway-info h3 {
                    color: #1e293b;
                    margin-bottom: 1rem;
                    font-size: 1.3rem;
                    font-weight: 700;
                }
                .gateway-info p {
                    color: #475569;
                    margin-bottom: 0.5rem;
                }
                .status-badge {
                    display: inline-block;
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    color: white;
                    padding: 0.4rem 1rem;
                    border-radius: 25px;
                    font-size: 0.8rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
                }
                .status-badge.dev {
                    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                    box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
                }
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 EveryCRED DCS</h1>
                <p class="subtitle">API Documentation Hub</p>
                
                <div class="api-grid">
                    <div class="api-card">
                        <div class="api-title">
                            🔐 API Version 1 
                            <span class="status-badge">Production Ready</span>
                        </div>
                        <div class="api-description">
                            Complete authentication system with Argon2 password hashing, 
                            user registration, login, and comprehensive health monitoring.
                        </div>
                        <div class="doc-links">
                            <a href="/api/v1/docs" class="doc-link">📚 Swagger UI</a>
                            <a href="/api/v1/redoc" class="doc-link redoc">📖 ReDoc</a>
                            <a href="/api/v1/openapi.json" class="doc-link openapi">⚙️ OpenAPI</a>
                        </div>
                    </div>
                    
                    <div class="api-card">
                        <div class="api-title">
                            🚀 API Version 2 
                            <span class="status-badge dev">In Development</span>
                        </div>
                        <div class="api-description">
                            Enhanced features and improved performance with advanced 
                            authentication mechanisms and future functionality.
                        </div>
                        <div class="doc-links">
                            <a href="/api/v2/docs" class="doc-link">📚 Swagger UI</a>
                            <a href="/api/v2/redoc" class="doc-link redoc">📖 ReDoc</a>
                            <a href="/api/v2/openapi.json" class="doc-link openapi">⚙️ OpenAPI</a>
                        </div>
                    </div>
                </div>
                
                <div class="gateway-info">
                    <h3>🌐 Gateway Information</h3>
                    <p><strong>Service:</strong> EveryCRED DCS API Gateway v1.0.0</p>
                    <p><strong>Environment:</strong> Development</p>
                    <p><strong>Status:</strong> <span class="status-badge">Healthy</span></p>
                    <div style="margin-top: 1.5rem;">
                        <a href="/health" class="doc-link">❤️ Health Check</a>
                        <a href="/api/status" class="doc-link openapi">📊 API Status</a>
                        <a href="/docs" class="doc-link redoc">📚 Gateway Docs</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    
    return app_


app = create_app()

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ThemeToggleDocsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject theme toggle functionality (light/dark mode) into Swagger UI docs pages.
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Check if this is a docs page request
        path = str(request.url.path)
        if "/docs" in path and response.status_code == 200:
            try:
                # Read response body
                if hasattr(response, "body_iterator"):
                    body_bytes = b""
                    async for chunk in response.body_iterator:
                        body_bytes += chunk
                elif hasattr(response, "body"):
                    body_bytes = response.body if isinstance(response.body, bytes) else response.body.encode()
                else:
                    return response
                
                # Decode HTML content
                html_content = body_bytes.decode("utf-8")
                
                # Inject script tag to load external JavaScript file with cache-busting
                # Use file modification time as cache buster to only reload when file changes
                static_dir = Path(__file__).parent.parent / "static"
                js_file = static_dir / "js" / "theme-toggle.js"
                cache_buster = int(js_file.stat().st_mtime) if js_file.exists() else int(time.time())
                script_tag = f'<script src="/static/js/theme-toggle.js?v={cache_buster}"></script>'
                
                # Inject script tag before closing head tag
                if "</head>" in html_content:
                    modified_html = html_content.replace("</head>", script_tag + "</head>")
                    return HTMLResponse(content=modified_html, status_code=200)
                
            except Exception:
                # If anything fails, return original response
                pass
        
        return response


# Add middleware to inject theme toggle functionality
# app.add_middleware(ThemeToggleDocsMiddleware)


# Exception handlers are now managed by the ErrorHandlerMiddleware and setup_error_handlers
