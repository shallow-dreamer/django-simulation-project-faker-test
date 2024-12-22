class ProcessingError(Exception):
    """
    参数处理异常
    """
    pass

class ValidationError(Exception):
    """
    参数验证异常
    """
    pass

class ParameterNotFoundError(Exception):
    """
    参数不存在异常
    """
    pass 