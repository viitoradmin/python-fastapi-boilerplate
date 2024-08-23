"""This module is an entry point for an application to run main application."""
import uvicorn
from app.core.config import settings
from app import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=int(settings.SERVER_PORT),
        reload=True
    )
