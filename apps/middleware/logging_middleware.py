from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log incoming request details
        print(f"Incoming request: {request.method} {request.url}")
        
        # Call the next middleware or endpoint
        response = await call_next(request)
        
        # Log response details
        print(f"Response status: {response.status_code}")
        return response
