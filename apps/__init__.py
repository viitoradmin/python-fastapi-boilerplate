from config import cors
from fastapi import FastAPI
from apps.constant import constant
from fastapi_versioning import VersionedFastAPI
from apps.api.view import defaultrouter, router

# Create app object and add routes
app = FastAPI(title="Python FastAPI ML boilerplate", middleware=cors.middleware)

# define router for different version
# router for version 1
app.include_router(
    defaultrouter, 
    prefix=constant.API_V1, tags=["/v1"]
    )
# router for version 2
app.include_router(
    router, prefix=constant.API_V2, tags=["/v2"]
    ) 

# Define version to specify version related API's.
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}", enable_latest=True)