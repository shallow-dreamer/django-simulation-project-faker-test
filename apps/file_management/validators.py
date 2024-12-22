from django.core.exceptions import ValidationError
import os
import magic

def validate_file_type(file):
    """
    验证文件类型
    """
    allowed_types = {
        'text/plain': '.txt',
        'application/vnd.ms-excel': '.xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/octet-stream': '.s2p'
    }
    
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    
    if file_type not in allowed_types:
        raise ValidationError(f'不支持的文件类型: {file_type}')

def validate_file_size(file):
    """
    验证文件大小
    """
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise ValidationError(f'文件大小不能超过 {max_size/1024/1024}MB') 