from fastapi import status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        if int(request.headers.get("content-length", 0)) > self.max_body_size:
            raise HTTPException(
                detail="Request entity too large",
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )
        return await call_next(request)