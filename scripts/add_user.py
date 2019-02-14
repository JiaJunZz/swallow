#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 10:47
# @Author  : ZJJ
# @Email   : 597105373@qq.com
import os
import django
import sys


project_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_name)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swallow.settings')
django.setup()
from django.contrib.auth import get_user_model
user = get_user_model()

for i in range(0,100):
    name = "dcy%s" %(i)
    user.objects.create(username=name,email=name+"@esunny.cc",password=name+"123456")
