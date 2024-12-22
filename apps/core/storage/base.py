from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, Dict, Any, List
from pathlib import Path

class StorageInterface(ABC):
    """
    存储接口定义
    """
    @abstractmethod
    def save(self, file: BinaryIO, path: str, **kwargs) -> str:
        """保存文件"""
        pass

    @abstractmethod
    def get(self, path: str) -> Optional[BinaryIO]:
        """获取文件"""
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        """删除文件"""
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        """检查文件是否存在"""
        pass

    @abstractmethod
    def url(self, path: str, **kwargs) -> str:
        """获取文件访问URL"""
        pass

class BaseStorage(StorageInterface):
    """
    存储基类
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_full_path(self, path: str) -> str:
        """获取完整路径"""
        return str(Path(self.config.get('base_path', '')).joinpath(path))

    def validate_file(self, file: BinaryIO) -> bool:
        """验证文件"""
        return True 