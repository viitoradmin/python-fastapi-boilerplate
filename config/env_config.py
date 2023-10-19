import os
from dotenv import load_dotenv
from os.path import join
from .project_path import BASE_DIR

##### ENV configuration  #####
dotenv_path = join(BASE_DIR, ".env")
load_dotenv(dotenv_path)




