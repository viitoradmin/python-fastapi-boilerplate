import os

from dotenv import load_dotenv

load_dotenv()

# Amazon s3 bucket credentials
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
EXPIRE_TIME = os.environ.get("EXPIRE_TIME")
REGION = os.environ.get("REGION")
LAMBDA_REGION = os.environ.get("LAMBDA_REGION")
PRIVATE_BUCKET = os.environ.get("PRIVATE_BUCKET")
PUBLIC_BUCKET = os.environ.get("PUBLIC_BUCKET")
AWS_BASE_URL = os.environ.get("AWS_BASE_URL")
PROXY_BASE_URL = os.environ.get("PROXY_BASE_URL")
