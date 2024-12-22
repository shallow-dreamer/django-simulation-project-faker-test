import os
import boto3
from typing import BinaryIO, Optional, Dict, Any
from abc import ABC, abstractmethod
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger('apps')

class BaseStorage(ABC):
    """
    存储服务基类
    """
    @abstractmethod
    def save_file(self, file: BinaryIO, filename: str, folder: str = '') -> str:
        """保存文件"""
        pass

    @abstractmethod
    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        """获取文件"""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        pass

    @abstractmethod
    def get_file_url(self, file_path: str, expires: int = 3600) -> str:
        """获取文件访问URL"""
        pass

class LocalStorage(BaseStorage):
    """
    本地文件存储
    """
    def __init__(self):
        self.storage = FileSystemStorage()
        self.base_path = settings.MEDIA_ROOT

    def save_file(self, file: BinaryIO, filename: str, folder: str = '') -> str:
        """
        保存文件到本地
        """
        file_path = os.path.join(folder, filename)
        return self.storage.save(file_path, file)

    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        """
        获取本地文件
        """
        try:
            return self.storage.open(file_path)
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None

    def delete_file(self, file_path: str) -> bool:
        """
        删除本地文件
        """
        try:
            self.storage.delete(file_path)
            return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False

    def get_file_url(self, file_path: str, expires: int = 3600) -> str:
        """
        获取本地文件URL
        """
        return self.storage.url(file_path)

class S3Storage(BaseStorage):
    """
    AWS S3存储
    """
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME

    def save_file(self, file: BinaryIO, filename: str, folder: str = '') -> str:
        """
        保存文件到S3
        """
        file_path = os.path.join(folder, filename)
        try:
            self.s3_client.upload_fileobj(file, self.bucket, file_path)
            return file_path
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        """
        从S3获取文件
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
            return response['Body']
        except ClientError as e:
            logger.error(f"Failed to get file from S3: {e}")
            return None

    def delete_file(self, file_path: str) -> bool:
        """
        从S3删除文件
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=file_path)
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False

    def get_file_url(self, file_path: str, expires: int = 3600) -> str:
        """
        获取S3文件的预签名URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': file_path
                },
                ExpiresIn=expires
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise 