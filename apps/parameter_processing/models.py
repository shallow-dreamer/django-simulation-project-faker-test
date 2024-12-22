from django.db import models
from apps.core.models import TimeStampedModel
from apps.file_management.models import UploadedFile
from django.utils.translation import gettext_lazy as _

class SParameter(TimeStampedModel):
    """S参数文件表"""
    file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name="s_parameters",
        verbose_name=_("S参数文件")
    )
    frequency = models.FloatField(_("频率"))
    value = models.JSONField(_("参数值"))

    class Meta:
        app_label = 'parameter_processing'
        verbose_name = _("S参数")
        verbose_name_plural = _("S参数")

class ParameterHistory(TimeStampedModel):
    """参数删除历史表"""
    parameter = models.ForeignKey(
        SParameter,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name=_("S参数")
    )
    operation = models.CharField(_("操作类型"), max_length=50)
    details = models.JSONField(_("操作详情"))

    class Meta:
        app_label = 'parameter_processing'
        verbose_name = _("参数历史")
        verbose_name_plural = _("参数历史") 