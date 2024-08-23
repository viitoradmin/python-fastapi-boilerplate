"""This module is creating Fastapi app instance with docs and redoc requiremnts."""
from fastapi import FastAPI

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

    application = FastAPI(title=settings.APP_NAME,
                          docs_url=None if settings.ENV_SERVER == settings.PRODUCTION_SERVER else "/docs",
                          redoc_url=None if settings.ENV_SERVER == settings.PRODUCTION_SERVER else "/redoc")
    application.include_router(router)

    return application
