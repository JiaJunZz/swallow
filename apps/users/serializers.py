#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 18:42
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    class Meta:
        model = User
        fields = ("id","username","email")
