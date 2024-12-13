import os
from os.path import join

from dotenv import load_dotenv

from .project_path import BASE_DIR

##### ENV configuration  #####
dotenv_path = join(BASE_DIR, ".env")
load_dotenv(dotenv_path)


## Database deatils ##
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")


## WKHTMLOPDF details ##
WKHTMLOPDF_PATH = os.environ.get("WKHTMLOPDF_PATH")
