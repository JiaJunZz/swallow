from django.db import models


# Create your models here.
class Idc(models.Model):
    """
    Idc模型
    """
    idc_name = models.CharField("机房名称", max_length=32, unique=True, help_text="机房名称")
    address = models.CharField("机房地址", null=True, max_length=128, help_text="机房地址")
    phone = models.CharField("机房电话", null=True, max_length=16, help_text="机房电话")
    remark = models.TextField("备注", null=True, max_length=255, help_text="备注")

    # create_date = models.DateTimeField(verbose_name=u'创建时间', blank=True, null=True, auto_now_add=True, max_length=32)
    # update_date = models.DateTimeField(verbose_name=u'更新时间', blank=True, null=True, auto_now=True, max_length=32)

    class Meta:
        verbose_name = 'IDC机房'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.idc_name


class Cabinet(models.Model):
    """
    机柜模型
    """
    idc = models.ForeignKey(Idc, verbose_name="所处机房", on_delete=models.CASCADE, null=True)
    cabinet_name = models.CharField("机柜号", max_length=10)

    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.cabinet_name
