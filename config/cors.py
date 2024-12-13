from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from core.utils import constant_variable

CORS_ALLOW_ORIGINS = ["*"]

CORS_ALLOW_METHODS = ["*"]

CORS_ALLOW_HEADERS = ["*"]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOW_ORIGINS,
        allow_credentials=constant_variable.STATUS_TRUE,
        allow_methods=CORS_ALLOW_METHODS,
        allow_headers=CORS_ALLOW_HEADERS,
    )
]
