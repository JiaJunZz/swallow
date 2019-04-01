#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 13:50
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from celery import Celery
from django.conf import settings
import os

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swallow.settings')

# 实例化Celery
app = Celery('swallow')

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')
