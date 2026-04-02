import logging
from typing import Any

import socketio
from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# from core.config import config
from config import project_path, LoggingConfig
from config.socket_config import SOCKETIO_PATH, get_socketio_server_kwargs
from core import CustomException
from core.utils import constant_variable
from middleware import S3PathMiddleware
from apps.v1.api.socket_io.view import register_default_handlers, router as socket_io_router

logger = logging.getLogger(__name__)


def init_routers(app_: FastAPI) -> None:
    app_.include_router(socket_io_router)
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

# Socket.IO server instance (set when create_socket_app is called)
_sio: socketio.AsyncServer | None = None


def get_sio() -> socketio.AsyncServer:
    """Return the Socket.IO server instance. Use for emitting from HTTP routes or background tasks."""
    if _sio is None:
        raise RuntimeError(
            "Socket.IO server not initialized. Call create_socket_app() first."
        )
    return _sio


def _normalize_socketio_path(path: str) -> str:
    p = (path or "").strip()
    if not p:
        return "/socket.io"
    return p if p.startswith("/") else f"/{p}"


def create_socket_app(fastapi_app: Any) -> socketio.ASGIApp:
    """
    Create Socket.IO AsyncServer, register handlers, and return an ASGI app
    that serves both Socket.IO (at SOCKETIO_PATH) and the given FastAPI app.
    """
    global _sio
    kwargs = get_socketio_server_kwargs()
    _sio = socketio.AsyncServer(**kwargs)
    register_default_handlers(_sio)

    socketio_path = _normalize_socketio_path(SOCKETIO_PATH)
    asgi_app = socketio.ASGIApp(_sio, fastapi_app, socketio_path=socketio_path)
    logger.info("Socket.IO mounted at path: %s", socketio_path)
    return asgi_app


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
