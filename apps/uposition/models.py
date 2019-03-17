from django.db import models
from idc.models import Cabinet
from server.models import Server

# Create your models here.
class Uposition(models.Model):
    """
    机柜U位模型
    """
    name = models.SmallIntegerField("U位", help_text="U位")
    cabinet = models.ForeignKey(Cabinet, verbose_name="所处机柜", on_delete=models.CASCADE, null=True, blank=True,
                                related_name='cab_u')
    server = models.ForeignKey(Server, verbose_name="服务器", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='u_server')

    class Meta:
        verbose_name = '机柜U位'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name