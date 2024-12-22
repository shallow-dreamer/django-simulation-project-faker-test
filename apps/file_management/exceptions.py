class FileUploadError(Exception):
    """
    文件上传异常
    """
    pass

class FileNotFoundError(Exception):
    """
    文件不存在异常
    """
    pass

class InvalidFileTypeError(Exception):
    """
    无效文件类型异常
    """
    pass

class CollectionNotFoundError(Exception):
    """
    收藏不存在异常
    """
    pass 