## ml_backend Directory explanations

- This machine learning directory contains modules and scripts related to machine learning backend functionality. 

* <I> Directory/Files to include </I>:

    1.       inference.py
    - Main script for making predictions using trained models.

    2.       ml_utils
    - This directory contains utility modules for machine learning operations.

    * <I> Directory/Files to include </I>:

        - ml_helper.py: Module containing helper functions for machine learning tasks.

    3.       ml_config
    - This directory contains configuration files for machine learning models.

    * <I> Directory/Files to include </I>:

        - ml_config.yaml: YAML file containing configuration parameters for models.

    4.       ml_models
    - This directory contains trained machine learning models.

    * <I> Directory/Files to include </I>:

        - your_model_files_here.pkl: Trained model files in pickle format.

    5.       ml_tools
    - This directory contains additional tools and scripts related to machine learning.

    Subdirectories in ml_tools {can add many more}:

    1.       llm
    -   Language Model related tools.
    2.       imagegen
    -   Image generation tools.
    3.       RAG
    -   Tools related to Retrieval-Augmented Generation.
    4.       csvreader
    -   Tools for reading and processing CSV files.
    5.       data_processing
    -   Tools for data preprocessing.
    6.       ml_experiment {.gitignore}
    -   This directory contains scripts and notebooks related 
to machine learning experiments.
    * <I> Directory/Files to include in ml_experiment</I>:
        1.       notebooks
        -  Jupyter notebooks for experimentation and analysis.
        1.       test-script.py
        -  Script for testing machine learning models or modules.
        1.       results
        -  Directory to store experiment results.

- <B> Note: Add ml_experiment directory add into .gitignore to avoid committing experimental files to version control.</B>

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
│   │       ├── test-script.py
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
