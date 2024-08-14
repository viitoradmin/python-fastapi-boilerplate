from fastapi import FastAPI, APIRouter
from .config import (
    AppSettings,
    EnvironmentOption,
    EnvironmentSettings,
    LLMSettings,
    settings
)

# ---------------------application-----------------------
def create_application(router, settings, **kwargs) -> FastAPI:
    """
    Creates and configures a FastAPI application based on the provided settings.

    This function initializes a FastAPI application and configures it with various settings and handlers based
    on the type of the `settings` object provided.

    Params:
        router: The APIRouter object containing the routes to be included in the FastAPI application.
        settings: An instance representing the settings for configuring the FastAPI application.
        **kwargs: Additional keyword arguments passed directly to the FastAPI constructor.

    Returns:
        FastAPI: A fully configured FastAPI application instance.

    """

    application = FastAPI()
    application.include_router(router)

    return application