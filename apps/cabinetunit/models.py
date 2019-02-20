from django.db import models
from idc.models import Cabinet
from server.models import Server

# Create your models here.
class CabinetUnit(models.Model):
    """
    机柜U位模型
    """
    u_number = models.CharField("U位", help_text="U位",max_length=2)
    cabinet = models.ForeignKey(Cabinet, verbose_name="所处机柜", on_delete=models.CASCADE, null=True, blank=True)
    server = models.ForeignKey(Server, verbose_name="服务器", on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = '机柜U位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.u_number
