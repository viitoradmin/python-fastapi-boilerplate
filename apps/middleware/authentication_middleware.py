from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse



class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secure_token: str):
        super().__init__(app)
        self.secure_token = secure_token

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        
        # Validate the Authorization token
        if not token or token != f"Bearer {self.secure_token}":
            return JSONResponse(content={"error": "Unauthorized"}, status_code=401)
        
        # Proceed to the next middleware or endpoint
        response = await call_next(request)
        return response
