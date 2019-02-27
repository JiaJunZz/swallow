from django.db import models


# Create your models here.

class Manufactory(models.Model):
    """
    厂商模型
    """
    manufactory_name = models.CharField("厂商名称", max_length=64, db_index=True, unique=True, help_text="厂商名称")
    phone = models.CharField("支持电话",blank=True, null=True, max_length=32, help_text="支持电话")
    remark = models.TextField("备注", blank=True, null=True, max_length=255, help_text="备注")

    # create_date = models.DateTimeField(verbose_name=u'创建时间', blank=True, null=True, auto_now_add=True, max_length=32)
    # update_date = models.DateTimeField(verbose_name=u'更新时间', blank=True, null=True, auto_now=True, max_length=32)

    class Meta:
        verbose_name = '制造商'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.manufactory_name


class ProductModel(models.Model):
    """
    产品型号模型
    """
    product_name = models.CharField("型号名称", max_length=10, help_text="型号名称")
    manufactory = models.ForeignKey(Manufactory, verbose_name="所属制造商", on_delete=models.CASCADE, help_text="所属制造商",
                                    null=True)

    class Meta:
        verbose_name = "产品型号"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.product_name
