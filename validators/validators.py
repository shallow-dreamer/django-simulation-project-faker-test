class FileValidator:
    """
    文件验证器
    
    设计考虑：
    1. 提供不同类型文件的格式验证
    2. 支持S参数文件和Com文件的特定验证
    3. 验证失败时提供详细的错误信息
    4. 可扩展性设计，易于添加新的验证规则
    """
    def validate_s_parameter_file(self, file):
        """
        验证S参数文件格式
        
        验证内容：
        1. 文件格式是否符合标准
        2. 频率范围是否有效
        3. 端口数量是否合理
        4. 数据完整性检查
        """
        pass
    
    def validate_com_file(self, file):
        """
        验证Com文件格式
        
        验证内容：
        1. 文件结构完整性
        2. 参数格式正确性
        3. 依赖关系有效性
        4. 数据范围合理性
        """
        pass 