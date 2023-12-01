<!-- PROJECT LOGO -->
<br />
<div align="center">
   <img src="images/python_logo.png" alt="Logo" width="80" height="80">

<h3 align="center">Python Fast API boilerplate</h3>

  <p align="center">
      Fast API boiler plate project 
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details  >
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

FastAPI boilerplate provides a simple basic structure for project creation with mysql database.


### Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]

<!-- GETTING STARTED -->
## Getting Started

Instructions for setting up project locally.
To get a local copy up and running follow these simple steps.

## Install + configure the project

### 1. Linux
### Prerequisites

Requirement of Project
* Install Python 
  ```sh
  Python-Version : 3.11.0
  ```
* Create python virtual environment
  ```sh
  python3 -m venv venv
  ```
* Activate the python virtual environment
  ```sh
  source venv/bin/activate
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/viitoradmin/python-fastapi-boilerplate/tree/feature/fastapi
   ```
2. Upgrade pip version
    ```sh
   python -m pip install --upgrade pip==22.1.2
    ```
3. Install the requirements for the project into the virtual environment
   ```sh
   pip install -r requirements.txt
   ```
4. Install the dependencies of Fast API
   ```sh
   pip install "fastapi[all]"
   ```

### 2. Windows

1. Create python virtual environment
   ```
   conda create --name venv python=3.11
   ```

2. Activate the python virtual environment
   ```
   conda activate venv
   ```

3. Install the requirements for the project into the virtual environment in the following sequence:
   ```
   pip install -r requirements.txt
   ```

4. Install the dependencies of Fast API
   ```
   pip install "fastapi[all]"
   ```

5. Upgrade pip version
   ```
   python -m pip install --upgrade pip==22.1.2
   ```

### Use the alembic to Upgrade/Downgrade the database in the FastAPI
  Note: Because by default Fastapi is provide only initial migrations. 
  It doesn't support the upgrade and downgrade the database.
   so,to perform automatic migrations follow the following steps:


1. To create Migration folder
    ```
    python -m alembic init migrations
    ```
2. Update the sqlalchemy.url into alembic.ini file
    ```
    sqlalchemy.url = mysql+pymysql://user:pass@host/db_name
    ```

3. update the Migrations>>env.py file o auto migrate the database.
    ```
    from models import Base 
    target_database = Base.metadata
    ```

4. Perform the initial migrations
    ```
    alembic revision --autogenerate -m 'initials'
    ```

5. Apply the changes into the database (upgrade the database)
    ```
    alembic upgrade head
    ```

6. To downgrade the database if required
    ```
    alembic downgrade -1
    ```

## Run the server in development mode
 
Add environment variables (given in .env) by running following command in cmd/terminal:

Run the server
   ```
   python asgi.py
   ```
Browse Swagger API Doc at: http://localhost:8000/docs

Browse  Redoc at: http://localhost:8000/redoc

Browse Swagger API Doc for version v1 at: http://localhost:8000/v1/docs

Browse Swagger API Doc for version v2 at: http://localhost:8000/v2/docs

## Release History

* 0.1
    * Work in progress

   
<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=Blue
[Python-url]: https://docs.python.org/3.10/
[FastAPI]: https://img.shields.io/badge/FastAPI-20232A?style=for-the-badge&logo=fastapi&logoColor=009485
[FastAPI-url]: https://fastapi.tiangolo.com/