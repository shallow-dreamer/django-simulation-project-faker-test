import os
import shutil
from typing import BinaryIO, Optional
from pathlib import Path
from django.conf import settings
from .base import BaseStorage

class LocalStorage(BaseStorage):
    """
    本地文件存储
    """
    def save(self, file: BinaryIO, path: str, **kwargs) -> str:
        full_path = self.get_full_path(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'wb') as dest:
            shutil.copyfileobj(file, dest)
        return path

    def get(self, path: str) -> Optional[BinaryIO]:
        full_path = self.get_full_path(path)
        try:
            return open(full_path, 'rb')
        except FileNotFoundError:
            return None

    def delete(self, path: str) -> bool:
        full_path = self.get_full_path(path)
        try:
            os.remove(full_path)
            return True
        except FileNotFoundError:
            return False

    def exists(self, path: str) -> bool:
        return os.path.exists(self.get_full_path(path))

    def url(self, path: str, **kwargs) -> str:
        return f"{settings.MEDIA_URL}{path}" 