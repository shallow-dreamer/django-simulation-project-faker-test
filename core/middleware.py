class SecurityMiddleware:
    """
    安全中间件
    
    设计考虑：
    1. 添加必要的安全响应头
    2. 防止常见的安全漏洞
    3. 遵循Django中间件规范
    4. 可配置的安全选项
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 处理请求
        response = self.get_response(request)
        
        # 添加安全响应头
        response['X-Content-Type-Options'] = 'nosniff'  # 防止MIME类型嗅探
        response['X-Frame-Options'] = 'DENY'  # 防止点击劫持
        
        return response 