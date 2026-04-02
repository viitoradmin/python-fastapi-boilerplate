import json
from typing import Any, Dict

import boto3
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from config import aws_config


class S3PathMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, config_path: str):
        super().__init__(app)
        self.s3_path_config = self._load_s3_config(config_path)

    def _load_s3_config(self, config_path: str) -> Dict:
        """
        Load dynamic S3 path configuration from a JSON file.
        """
        try:
            with open(config_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise RuntimeError(f"S3 path configuration file not found: {config_path}")
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Invalid JSON format in S3 path configuration: {config_path}"
            )

    def resolve_s3_path(self, file_type: str, file_name: str) -> str:
        """
        Resolve the S3 path dynamically based on file type and file extension.
        """
        file_extension = file_name.split(".")[-1]  # Extract file extension
        type_config = self.s3_path_config.get("paths", {}).get(file_type, {})
        # Match by file extension
        path = type_config.get(file_extension, type_config.get("default"))
        if not path:
            raise ValueError(
                f"No path found for file type '{file_type}' and extension '{file_extension}'"
            )
        return f"{path}/{file_name}"

    def get_s3_client(self):
        """Create an S3 client."""
        return boto3.client(
            "s3",
            aws_access_key_id=aws_config.AWS_ACCESS_KEY,
            aws_secret_access_key=aws_config.AWS_SECRET_KEY,
            region_name=aws_config.REGION,
        )

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """
        Process the request and modify the response with resolved S3 paths.
        """
        # Attach S3 client to the request state
        request.state.s3_client = self.get_s3_client()

        response = await call_next(request)
        return response
