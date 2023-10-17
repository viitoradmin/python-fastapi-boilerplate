from config import cors
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from apps.api.auth.view import defaultrouter

# Create app object and add routes
app = FastAPI(title="Python FastAPI boilerplate", middleware=cors.middleware)

# define router for different version
app.include_router(defaultrouter) # router for version 1

# Define version to specify version related API's.
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}", enable_latest=True)