"""This module is include API's route."""
from fastapi import FastAPI

from apps.api.auth.models import Base as authbase
from apps.api.auth.view import router
from apps.constant import constant
from config import cors, database
from apps.middleware.custom_middleware import CustomMiddleware
from apps.middleware.request_size_middleware import LimitRequestSizeMiddleware
from apps.middleware.logging_middleware import LogRequestsMiddleware
from apps.middleware.authentication_middleware import AuthMiddleware
from apps.middleware.session_middleware import SessionMiddleware
from apps.middleware.rate_limiting_middleware import RateLimitMiddleware
from apps.middleware.error_handling_middleware import ErrorHandlingMiddleware

# Bind with the database, whenever new models find it's create it.
authbase.metadata.create_all(bind=database.engine)

# Create app object and add routes
app = FastAPI(title="Python FastAPI boilerplate", middleware=cors.middleware)

# add middlewares
app.add_middleware(CustomMiddleware)
app.add_middleware(LimitRequestSizeMiddleware, max_body_size=10 * 1024 * 1024)
app.add_middleware(LogRequestsMiddleware)
app.add_middleware(AuthMiddleware, secure_token="secure_token")
app.add_middleware(SessionMiddleware, secure_token="new_session_token")
app.add_middleware(RateLimitMiddleware, rate_limit=5, time_window=60)
app.add_middleware(ErrorHandlingMiddleware)

# define router for different version
# router for API's
app.include_router(
    router,
    prefix=constant.API_V1
    )
