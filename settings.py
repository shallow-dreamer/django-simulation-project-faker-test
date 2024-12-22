INSTALLED_APPS = [
    # Django内置应用
    'rest_framework',  # REST框架支持
    
    # 自定义应用
    'users',          # 用户管理
    'files',          # 文件基础功能
    's_parameters',   # S参数处理
    'com_simulation', # Com仿真
    'serder_simulation', # Serder仿真
    'fom_chi',       # Fom_chi计算
    'collections',    # 收藏功能
    'third_party',   # 第三方平台集成
]

# REST框架配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # JWT认证
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 默认需要认证
    ],
} 