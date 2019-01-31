#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 18:42
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """
    用户序列化类
    """
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
