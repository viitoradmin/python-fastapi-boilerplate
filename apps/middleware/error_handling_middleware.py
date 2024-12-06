from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Proceed to the next middleware or endpoint
            response = await call_next(request)
            return response
        except Exception as exc:
            # Catch any exception and return a JSON response with status 500
            return JSONResponse(content={"error": str(exc)}, status_code=500)
