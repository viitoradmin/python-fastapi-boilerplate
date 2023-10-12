import os
import uvicorn
from apps.__init__ import app
from config.env_config import load_dotenv

load_dotenv()

if __name__ == "__main__":
    uvicorn.run("asgi:app",
                host=os.environ.get('SERVER_HOST'),
                port=int(os.environ.get('SERVER_PORT')),
                reload=True)