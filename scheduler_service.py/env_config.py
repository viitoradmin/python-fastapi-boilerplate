from os.path import abspath, dirname, join

from dotenv import load_dotenv

# ##### PATH CONFIGURATION ################################

# fetch FastAPI's project directory
BASE_DIR = dirname(abspath(__file__))

# ##### ENV CONFIGURATION ################################

# Take environment variables from .env file
dotenv_path = join(BASE_DIR, ".env")
load_dotenv(dotenv_path)
