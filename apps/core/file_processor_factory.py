from typing import Dict, Type
from apps.core.file_processors import BaseFileProcessor, TouchstoneProcessor, ExcelProcessor

class FileProcessorFactory:
    """
    文件处理器工厂
    """
    _processors: Dict[str, Type[BaseFileProcessor]] = {
        '.s2p': TouchstoneProcessor,
        '.xlsx': ExcelProcessor,
        '.xls': ExcelProcessor
    }
    
    @classmethod
    def get_processor(cls, file_extension: str) -> BaseFileProcessor:
        """
        获取文件处理器
        """
        processor_class = cls._processors.get(file_extension.lower())
        if not processor_class:
            raise ValueError(f"Unsupported file type: {file_extension}")
        return processor_class() 