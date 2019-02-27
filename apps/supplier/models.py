from django.db import models


# Create your models here.

class Supplier(models.Model):
    """
    供应商模型
    """
    supplier_name = models.CharField('供应商名称', max_length=64, unique=True, help_text="供应商名称")
    phone = models.CharField('支持电话', blank=True, null=True, max_length=16, help_text="支持电话")
    remark = models.TextField("备注", null=True, blank=True, max_length=255, help_text="备注")

    # create_date = models.DateTimeField(verbose_name=u'创建时间', blank=True, null=True, auto_now_add=True, max_length=32)
    # update_date = models.DateTimeField(verbose_name=u'更新时间', blank=True, null=True, auto_now=True, max_length=32)

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.supplier_name
