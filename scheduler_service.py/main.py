import os
import constant
import uvicorn
from scheduler import app

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ.get("SERVER_HOST"),
        port=int(os.environ.get("SERVER_PORT")),
        reload=constant.STATUS_TRUE,
    )
