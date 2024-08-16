# FastAPI LLM Boilerplate
## Overview
This repository contains a FastAPI application designed to serve as a backend for Large Language Models (LLMs). The application provides a robust API for interacting with LLMs, enabling various functionalities such as text generation, processing, and custom actions based on LLM outputs. The architecture follows best practices and coding standards, and it is structured to be scalable and easy to integrate with other systems.

## Built With

* [![Python][Python]][Python-url]
* [![FastAPI][FastAPI]][FastAPI-url]

## Features
- LLM Integration: Seamlessly integrate with LLMs like OpenAI's GPT models.
- Custom Actions: Define and execute custom actions based on LLM's structured outputs.
- Flexible API: Expose endpoints for various LLM-related functionalities.

## Installation
To get started with this application, clone the repository and install the required dependencies.
```bash
$ git clone https://github.com/viitoradmin/python-fastapi-boilerplate.git
$ cd python-fastapi-boilerplate
$ python -m venv venv
$ source venv\bin\activate
$ pip install -r requirements.txt
```

Copy environment variables and add your credentials.
```bash
$ cp .env.example .env
```

## Run the server
```bash
$ python main.py
```

<!-- MARKDOWN LINKS & IMAGES -->
[Python]: https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=Blue
[Python-url]: https://docs.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-20232A?style=for-the-badge&logo=fastapi&logoColor=009485
[FastAPI-url]: https://fastapi.tiangolo.com/