from config import cors
from fastapi import FastAPI
from config import database
from apps.constant import constant
from fastapi_versioning import VersionedFastAPI
from apps.api.auth.view import router_v1, router_v2
from apps.api.auth.models import Base as authbase

# Bind with the database, whenever new models find it's create it.
authbase.metadata.create_all(bind=database.engine)

# Create app object and add routes
app = FastAPI(title="Python FastAPI boilerplate", middleware=cors.middleware)

# define router for different version
# router for version 1
app.include_router(
    router_v1, 
    prefix=constant.API_V1, tags=["/v1"]
    )
# router for version 2
app.include_router(
    router_v2, 
    prefix=constant.API_V2, tags=["/v2"]
    )

# Define version to specify version related API's.
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")