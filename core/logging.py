import logging

logger = logging.getLogger(__name__)

class OperationLogger:
    """
    操作日志记录器
    
    设计考虑：
    1. 统一的日志记录接口
    2. 记录用户操作，便于审计和追踪
    3. 使用Python标准logging模块，便于集成
    4. 支持不同级别的日志记录
    """
    @staticmethod
    def log_operation(user, operation, status):
        """
        记录用户操作
        
        参数：
        - user: 执行操作的用户
        - operation: 操作描述
        - status: 操作状态
        """
        logger.info(f"User {user} performed {operation}: {status}") 