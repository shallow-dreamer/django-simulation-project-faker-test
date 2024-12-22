from django.db import models
from apps.core.models import TimeStampedModel
from apps.parameter_processing.models import SParameter
from django.utils.translation import gettext_lazy as _

class ComSimulation(TimeStampedModel):
    """Com仿真模型"""
    name = models.CharField(_("仿真名称"), max_length=255)
    parameters = models.ManyToManyField(
        SParameter,
        related_name="com_simulations",
        verbose_name=_("使用的参数")
    )
    configuration = models.JSONField(_("仿真配置"))
    status = models.CharField(_("仿真状态"), max_length=50)
    result = models.JSONField(_("仿真结果"), null=True, blank=True)

    class Meta:
        app_label = 'com_simulation'
        verbose_name = _("Com仿真")
        verbose_name_plural = _("Com仿真")

class SimulationHistory(TimeStampedModel):
    """仿真历史记录"""
    simulation = models.ForeignKey(
        ComSimulation,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name=_("仿真")
    )
    execution_time = models.FloatField(_("执行时间"))
    status = models.CharField(_("执行状态"), max_length=50)
    error_message = models.TextField(_("错误信息"), null=True, blank=True)

    class Meta:
        app_label = 'com_simulation'
        verbose_name = _("仿真历史")
        verbose_name_plural = _("仿真历史") 