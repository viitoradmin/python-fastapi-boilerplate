from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from time import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int, time_window: int = 60):
        """
        :param app: The FastAPI app
        :param rate_limit: Maximum number of requests allowed
        :param time_window: Time window in seconds for rate limiting (default is 60 seconds)
        """
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_count = 0
        self.window_start_time = time()

    async def dispatch(self, request: Request, call_next):
        current_time = time()

        # Check if the time window has expired
        if current_time - self.window_start_time > self.time_window:
            # Reset the window
            self.window_start_time = current_time
            self.request_count = 0

        # Enforce rate limiting
        if self.request_count >= self.rate_limit:
            return JSONResponse(
                content={"error": "Rate limit exceeded"}, status_code=429
            )

        # Increment request count
        self.request_count += 1

        # Process the request
        response = await call_next(request)
        return response