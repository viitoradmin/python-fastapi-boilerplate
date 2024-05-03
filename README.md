<!-- PROJECT LOGO -->
<br />
<div align="center">
   <img src="images/python_logo.png" alt="Logo" width="80" height="80">

<h3 align="center">Python Fast API Boilerplate</h3>

  <p align="center">
      Fast API Boilerplate Project 
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

## Repository Structure

```sh
├── apps
│   ├── api
│   │   ├── __init__.py
│   │   └── view.py
│   ├── constant
│   │   ├── __init__.py
│   │   └── constant.py
│   ├── ml_backend
│   │   ├── __init__.py
│   │   ├── inference.py
│   │   ├── ml_utils
│   │   │   ├── __init__.py
│   │   │   └── ml_helper.py
│   │   ├── ml_config
│   │   │   ├── ml_config.yaml
│   │   ├── ml_models
│   │   │   ├── __init__.py
│   │   │   └── your_model_files_here.pkl
│   │   ├── ml_tools
│   │   │   ├── llm # directory
│   │   │   ├── imagegen # directory
│   │   │   ├── RAG # directory
│   │   │   ├── csvreader # directory
│   │   │   └── data_processing # directory
│   │   └── ml_experiment  # add into gitignore
│   │       ├── notebooks # directory
│   │       ├── test-script.py # directory
│   │       └── results # directory
│   ├── utils
│   │   ├── __init__.py
│   │   ├── helper.py
│   │   ├── message.py
│   │   └── standard_response.py
│   └── __init__.py
├── config
│   ├── __init__.py
│   ├── cors.py
│   ├── env_config.py
│   └── project_path.py
├── data
│   ├── __init__.py
│   ├── your_data_files_here.csv
│   └── other_data_folders_here
├── images
│   ├── Logo1.webp
│   └── python_logo2.png
├── models
│   ├── __init__.py
│   └── your_other_model_files_here.pth
├── tests
│   ├── __init__.py
│   └── your_test_files_here.py
├── static
│   ├── __init__.py
│   └── your_static_files_here.css
├── templates
│   ├── __init__.py
│   └── your_html_template_files_here.html
├── asgi.py
├── README.md
└── requirements.txt
```

---

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
   git clone https://github.com/viitoradmin/python-fastapi-boilerplate
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