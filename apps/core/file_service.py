from typing import BinaryIO, Optional, Dict, Any
from django.core.files.uploadedfile import UploadedFile
from apps.core.storage_factory import StorageFactory
from apps.core.file_processor_factory import FileProcessorFactory
import os
import uuid
import logging

logger = logging.getLogger('apps')

class FileService:
    """
    文件服务
    """
    def __init__(self):
        self.storage = StorageFactory.get_storage()

    def save_uploaded_file(self, file: UploadedFile, folder: str = '') -> Dict[str, str]:
        """
        保存上传的文件
        """
        try:
            # 验证文件
            self._validate_file(file)
            
            # 生成唯一文件名
            ext = os.path.splitext(file.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            
            # 保存文件
            file_path = self.storage.save_file(file, filename, folder)
            
            # 处理文件内容
            processed_data = self._process_file(file, ext)
            
            return {
                'file_path': file_path,
                'original_name': file.name,
                'file_type': file.content_type,
                'file_size': file.size,
                'processed_data': processed_data
            }
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {e}")
            raise

    def _validate_file(self, file: UploadedFile) -> None:
        """
        验证文件
        """
        # 获取文件扩展名
        ext = os.path.splitext(file.name)[1]
        
        try:
            # 获取处理器
            processor = FileProcessorFactory.get_processor(ext)
            
            # 验证文件格式
            if not processor.validate(file):
                raise ValueError(f"Invalid file format for {ext}")
            
            # 重置文件指针
            file.seek(0)
            
        except Exception as e:
            logger.error(f"File validation failed: {e}")
            raise

    def _process_file(self, file: UploadedFile, ext: str) -> Dict[str, Any]:
        """
        处理文件内容
        """
        try:
            # 获取处理器
            processor = FileProcessorFactory.get_processor(ext)
            
            # 处理文件
            result = processor.process(file)
            
            # 重置文件指针
            file.seek(0)
            
            return result
        except Exception as e:
            logger.error(f"File processing failed: {e}")
            raise

    def get_file_content(self, file_path: str) -> Optional[BinaryIO]:
        """
        获取文件内容
        """
        return self.storage.get_file(file_path)

    def delete_file(self, file_path: str) -> bool:
        """
        删除文件
        """
        return self.storage.delete_file(file_path)

    def get_file_url(self, file_path: str, expires: int = 3600) -> str:
        """
        获取文件访问URL
        """
        return self.storage.get_file_url(file_path, expires)

    def move_file(self, source_path: str, target_path: str) -> bool:
        """
        移动文件
        """
        try:
            # 获取源文件
            file_content = self.get_file_content(source_path)
            if not file_content:
                return False
            
            # 保存到新位置
            self.storage.save_file(file_content, os.path.basename(target_path),
                                 os.path.dirname(target_path))
            
            # 删除原文件
            self.delete_file(source_path)
            
            return True
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return False 