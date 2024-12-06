from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, new_session_token: str):
        super().__init__(app)
        self.new_session_token = new_session_token

    async def dispatch(self, request: Request, call_next):
        # Check for the session token in cookies
        session_token = request.cookies.get("session_token")
        if not session_token:
            # Return a response indicating the session has expired
            response = JSONResponse(content={"error": "Session expired"}, status_code=403)
            # Set a new session token in the cookies
            response.set_cookie(key="session_token", value=self.new_session_token)
            return response
        
        # Proceed to the next middleware or endpoint
        response = await call_next(request)
        return response
