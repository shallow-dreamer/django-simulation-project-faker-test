import os
from typing import BinaryIO
from django.core.files.storage import default_storage
from django.conf import settings
from apps.core.services import BaseService
from apps.file_management.models import UploadedFile, FileCollection
from apps.core.file_service import FileService
from django.core.files.uploadedfile import UploadedFile as DjangoUploadedFile
import logging

logger = logging.getLogger('apps')

class FileManagementService(BaseService):
    """
    文件管理服务
    """
    def __init__(self):
        self.file_service = FileService()

    def handle_file_upload(self, file: DjangoUploadedFile, user) -> UploadedFile:
        """
        处理文件上传
        """
        # 保存文件
        file_info = self.file_service.save_uploaded_file(
            file,
            folder=f'user_{user.id}'
        )
        
        # 创建文件记录
        return UploadedFile.objects.create(
            file=file_info['file_path'],
            name=file_info['original_name'],
            file_type=file_info['file_type'],
            user=user
        )

    def add_to_collection(self, file: UploadedFile, collection: FileCollection) -> bool:
        """
        将文件添加到收藏
        """
        try:
            # 移动文件到收藏目录
            new_path = f'collections/{collection.id}/{os.path.basename(file.file.name)}'
            if self.file_service.move_file(file.file.name, new_path):
                file.file = new_path
                file.collection = collection
                file.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to add file to collection: {e}")
            return False 