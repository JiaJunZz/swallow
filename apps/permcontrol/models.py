from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, blank=True, help_text="用户名")
    phone = models.CharField("电话", blank=True, null=True, max_length=16, help_text="电话")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
