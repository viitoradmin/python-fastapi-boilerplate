import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# from core.config import config
from config import project_path, LoggingConfig
from core import CustomException
from core.utils import constant_variable
from middleware import S3PathMiddleware


def init_routers(app_: FastAPI) -> None:
    pass
    # app_.include_router(user_router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        content = {"status": exc.status, "data": exc.data, "message": exc.message}
        return JSONResponse(
            status_code=exc.status,
            content=content,
        )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=constant_variable.STATUS_TRUE,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            S3PathMiddleware, config_path=f"{project_path.S3_ROOT}/s3_paths_config.json"
        ),
    ]
    return middleware


# TODO: Redis Cache Implement


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        # docs_url=None if config.ENV == "production" else "/docs",
        # redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(LoggingConfig().get_config)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    # init_cache() # Redis Cache Implement
    return app_


app = create_app()
logger = logging.getLogger(__name__)
