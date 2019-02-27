#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from django.contrib.auth.models import Group
from users.serializers import UserSerializer


class GroupsSerializer(serializers.ModelSerializer):
    """
    Groups序列化类
    """
    user_set = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name","user_set")
