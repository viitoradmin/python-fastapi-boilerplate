# FastAPI boilerplate

## 🛠 Skills
Python, Fask-API, Swagger Doc, Html and Java Scripts.

## Install + configure the project

### 1. Linux
```
# Create python virtual environment
python3 -m venv venv

# Activate the python virtual environment
source venv/bin/activate

# Install the requirements for the project into the virtual environment
pip install -r requirements.txt

# Install the dependencies of Fast API
pip install "fastapi[all]"

# Upgrade pip version
python -m pip install --upgrade pip==22.1.2
```
### 2. Windows
```
# Create python virtual environment
conda create --name venv python=3.10.12

# Activate the python virtual environment
conda activate venv

# Install the requirements for the project into the virtual environment in the following sequence:
pip install -r requirements.txt

# Install the dependencies of Fast API
pip install "fastapi[all]"

# Upgrade pip version
python -m pip install --upgrade pip==22.1.2
```

## Use the alembic to Upgrade/Downgrade the database in the FastAPI
Note: Because by default Fastapi is provide only initial migrations. It doesn't support the upgrade and downgrade the database.
so,to perform automatic migrations follow the following steps:

1. # To create Migration folder
python -m alembic init migrations

2. ## update the Migrations>>env.py file o auto migrate the database.
from models import Base
target_database = Base.metadata

4. # Perform the initial migrations
alembic revision --autogenerate -m 'initials'

5. # Apply the changes into the database (upgrade the database)
alembic upgrade head
   # To downgrade the database if required
   alembic downgrade -1

## Run the server in development mode
 
Add environment variables (given in .env) by running following command in cmd/terminal:

Run the server
```
python asgi.py
```
Browse Swagger API Doc at: http://localhost:8000/docs
Browse  Redoc at: http://localhost:8000/redoc

## Release History

* 0.1
    * Work in progress