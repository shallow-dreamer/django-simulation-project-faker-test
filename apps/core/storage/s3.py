from typing import BinaryIO, Optional
import boto3
from botocore.exceptions import ClientError
from .base import BaseStorage

class S3Storage(BaseStorage):
    """
    AWS S3存储
    """
    def __init__(self, config):
        super().__init__(config)
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config['region_name']
        )
        self.bucket = config['bucket_name']

    def save(self, file: BinaryIO, path: str, **kwargs) -> str:
        try:
            self.s3.upload_fileobj(file, self.bucket, path)
            return path
        except ClientError:
            raise

    def get(self, path: str) -> Optional[BinaryIO]:
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=path)
            return response['Body']
        except ClientError:
            return None

    def delete(self, path: str) -> bool:
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=path)
            return True
        except ClientError:
            return False

    def exists(self, path: str) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket, Key=path)
            return True
        except ClientError:
            return False

    def url(self, path: str, **kwargs) -> str:
        expires = kwargs.get('expires', 3600)
        try:
            return self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': path},
                ExpiresIn=expires
            )
        except ClientError:
            raise 