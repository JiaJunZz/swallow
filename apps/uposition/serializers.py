#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Uposition


class UpositionSerializer(serializers.ModelSerializer):
    """
     U位序列化类
    """

    class Meta:
        model = Uposition
        fields = ['id', 'name', 'cabinet', 'server']
        validators = [
            UniqueTogetherValidator(
                queryset=Uposition.objects.all(),
                fields=('name', 'cabinet'),
                message='此U位已经存在'
            )
        ]


class UpositionNoCabinetSerializer(serializers.ModelSerializer):
    """
    U位序列化类
    无cabinet
    """

    class Meta:
        model = Uposition
        fields = ['id', 'name']

