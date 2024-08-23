"""This module contains function to run the application with the specified routes."""
from app.api import router
from app.core.config import settings
from app.core.setup import create_application

app = create_application(router=router, settings=settings)
