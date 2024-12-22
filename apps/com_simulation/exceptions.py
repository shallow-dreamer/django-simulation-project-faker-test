class SimulationError(Exception):
    """
    仿真异常
    """
    pass

class ConfigurationError(Exception):
    """
    配置错误异常
    """
    pass

class SimulationNotFoundError(Exception):
    """
    仿真不存在异常
    """
    pass 