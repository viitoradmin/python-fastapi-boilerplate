from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from apps.api.auth.v1.view import router
from apps.api.auth.v2.view import authrouter
from config import cors

# Create app object and add routes
app = FastAPI(title="Python FastAPI boilerplate", middleware=cors.middleware)

# define router for different version
app.include_router(router, prefix="/v1", tags=["v1"]) # router for version 1
app.include_router(authrouter, prefix="/v2", tags=["v2"]) # router for version 2

# # # Define version to specify version related API's.
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}", enable_latest=True)