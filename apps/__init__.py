from config import cors
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from apps.api.view import router
from apps.constant import constant

# Create FastAPI app object and add middleware for CORS
app = FastAPI(title="Calenso ML", middleware=cors.middleware)

# Define versioning for the API using VersionedFastAPI
app = VersionedFastAPI(
    app, version_format="{major}", prefix_format="/v{major}", enable_latest=True
)

# Include HTTP routes for version 2
app.include_router(router, prefix=constant.API_V2, tags=["/v2"])

# Include HTTP routes for the default version
app.include_router(router)

# Include WebSocket route
# Note: WebSocket routes should be separate from HTTP routes
app.include_router(router, prefix="/ws", tags=["websocket"])
