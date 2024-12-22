from django.core.exceptions import ValidationError
from django.db import transaction
from .models import ExternalPlatform, ExternalFileReference

class ExternalReferenceService:
    """
    外部文件引用服务类
    
    设计考虑：
    1. 使用事务确保数据一致性
    2. 支持文件引用创建的同时导入文件数据
    3. 根据文件类型自动分发到对应的模型
    4. 异常处理确保操作的安全性
    """
    
    @staticmethod
    def create_reference(platform_name: str, external_url: str, reference_id: str, 
                        file_name: str, file_type: str, user, file_data=None) -> ExternalFileReference:
        """
        创建外部文件引用，并可选择性导入数据
        
        参数说明：
        - platform_name: 外部平台名称
        - external_url: 文件在外部平台的URL
        - reference_id: 外部平台的文件标识
        - file_name: 文件名
        - file_type: 文件类型
        - user: 创建用户
        - file_data: 可选的文件数据，用于导入
        """
        try:
            # 验证平台是否存在且激活
            platform = ExternalPlatform.objects.get(name=platform_name, is_active=True)
        except ExternalPlatform.DoesNotExist:
            raise ValidationError(f"Platform {platform_name} not found or inactive")

        with transaction.atomic():
            # 创建外部引用记录
            reference = ExternalFileReference.objects.create(
                platform=platform,
                external_url=external_url,
                reference_id=reference_id,
                file_name=file_name,
                file_type=file_type,
                created_by=user
            )

            # 如果提供了文件数据，根据类型导入到对应的表
            if file_data:
                # 根据文件类型创建对应的文件记录
                if file_type == 's_parameter':
                    from s_parameters.models import SParameterFile
                    imported_file = SParameterFile.objects.create(
                        name=file_name,
                        file=file_data,
                        user=user,
                        source_type='EXTERNAL',
                        source_url=external_url,
                        source_reference=reference_id
                    )
                elif file_type == 'com':
                    from com_simulation.models import ComFile
                    imported_file = ComFile.objects.create(
                        name=file_name,
                        file=file_data,
                        user=user,
                        source_type='EXTERNAL',
                        source_url=external_url,
                        source_reference=reference_id
                    )
                # 可以继续添加其他文件类型的处理...

            return reference

    @staticmethod
    def get_reference(platform_name: str, reference_id: str) -> ExternalFileReference:
        """获取外部文件引用"""
        try:
            return ExternalFileReference.objects.get(
                platform__name=platform_name,
                reference_id=reference_id
            )
        except ExternalFileReference.DoesNotExist:
            raise ValidationError(f"Reference not found") 