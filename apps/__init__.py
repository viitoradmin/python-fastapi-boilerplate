"""This module is include API's route."""
from fastapi import FastAPI

from apps.api.auth.models import Base as authbase
from apps.api.auth.view import router
from apps.constant import constant
from config import cors, database

# Bind with the database, whenever new models find it's create it.
authbase.metadata.create_all(bind=database.engine)

# Create app object and add routes
app = FastAPI(title="Python FastAPI boilerplate", middleware=cors.middleware)

# define router for different version
# router for API's
app.include_router(
    router,
    prefix=constant.API_V1
    )
