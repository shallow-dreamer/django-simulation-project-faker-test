from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

class FileCollection(TimeStampedModel):
    """收藏表模型"""
    class Meta:
        app_label = 'file_management'
        verbose_name = _("收藏表")
        verbose_name_plural = _("收藏表")

    name = models.CharField(_("收藏名称"), max_length=255)
    description = models.TextField(_("描述"), blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collections",
        verbose_name=_("用户")
    )

class UploadedFile(TimeStampedModel):
    """上传文件模型"""
    class Meta:
        app_label = 'file_management'
        verbose_name = _("上传文件")
        verbose_name_plural = _("上传文件")

    file = models.FileField(_("文件"), upload_to="uploads/%Y/%m/%d/")
    name = models.CharField(_("文件名"), max_length=255)
    file_type = models.CharField(_("文件类型"), max_length=50)
    collection = models.ForeignKey(
        FileCollection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="files",
        verbose_name=_("所属收藏")
    )
 