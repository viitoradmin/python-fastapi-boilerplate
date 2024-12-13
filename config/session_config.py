import os

# Constants
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
SESSION_TIMEOUT = 3600  # 1 hour
