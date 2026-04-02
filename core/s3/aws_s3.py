from typing import List, Optional

from botocore.exceptions import ClientError
from fastapi import Request

from config import aws_config


class S3Manager:
    """
    A class to manage S3 operations with dynamic path resolution.
    """

    bucket_name = aws_config.PUBLIC_BUCKET
    region = aws_config.REGION

    def __init__(self, request: Request):
        self.s3_client = request.state.s3_client

    def upload_file(
        self,
        file_obj,
        s3_path: str,
        content_type: Optional[str] = None,
    ) -> str:
        """
        Upload a file to a dynamically resolved S3 path.
        """
        # s3_path = f"{self.resolve_path(file_type)}/{file_name}"
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_path,
                ExtraArgs={"ContentType": content_type} if content_type else None,
            )
            return s3_path
        except ClientError as e:
            raise RuntimeError(f"Failed to upload file to S3: {str(e)}")

    def generate_presigned_url(self, s3_path: str, expiration: int = 3600) -> str:
        """
        Generate a pre-signed URL for accessing a file.
        """
        try:
            return self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_path},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            raise RuntimeError(f"Failed to generate pre-signed URL: {str(e)}")

    def list_files(self, prefix: str) -> List[str]:
        """
        List files in a specific S3 path (prefix).
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )
            return [item["Key"] for item in response.get("Contents", [])]
        except ClientError as e:
            raise RuntimeError(f"Failed to list files in S3: {str(e)}")

    def delete_file(self, s3_path: str) -> None:
        """
        Delete a file from S3.
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_path)
        except ClientError as e:
            raise RuntimeError(f"Failed to delete file from S3: {str(e)}")
