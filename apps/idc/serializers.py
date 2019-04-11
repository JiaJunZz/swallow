#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Idc, Cabinet


class CabinetSerializer(serializers.ModelSerializer):
    """
    Cabinet序列化类
    depth
    """

    class Meta:
        model = Cabinet
        fields = ['id', 'name']
        depth = 2


class CabinetNodepthSerializer(serializers.ModelSerializer):
    """
    Cabinet序列化类
    No depth
    """

    class Meta:
        model = Cabinet
        fields = ['id', 'name', 'idc']
        validators = [
            UniqueTogetherValidator(
                queryset=Cabinet.objects.all(),
                fields=('name', 'idc'),
                message="此机柜号存在"
            )
        ]

    def create(self, validated_data):
        cabinet_obj = Cabinet.objects.create(**validated_data)
        self.create_uposition(cabinet_obj)
        return cabinet_obj

    @staticmethod
    def create_uposition(cabinet_obj):
        for i in range(1, 43):
            cabinet_obj.cab_u.create(name=i)


class IdcSerializer(serializers.ModelSerializer):
    """
    Idc序列化类
    """

    idc_cab = CabinetSerializer(read_only=True, many=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建时间", help_text="创建时间", required=False,
                                            read_only=True)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="更新时间", help_text="更新时间", required=False,
                                            read_only=True)

    class Meta:
        model = Idc
        fields = ['id', 'name', 'address', 'phone', 'remark', 'idc_cab', 'create_date', 'update_date']
        depth = 2
