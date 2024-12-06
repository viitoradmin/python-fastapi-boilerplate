from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Logic before processing the request
        print("Before Request")
        
        response = await call_next(request)
        
        # Logic after processing the request
        print("After Request")
        return response


