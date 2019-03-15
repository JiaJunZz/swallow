#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Idc, Cabinet, Uposition


class UpositionSerializer(serializers.ModelSerializer):
    """
     U位序列化类
    """

    class Meta:
        model = Uposition
        fields = ['id', 'u_name', 'cabinet', 'server']
        validators = [
            UniqueTogetherValidator(
                queryset=Uposition.objects.all(),
                fields=('u_name', 'cabinet'),
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
        fields = ['id', 'u_name']


class CabinetSerializer(serializers.ModelSerializer):
    """
    Cabinet序列化类
    depth
    """
    uposition = UpositionNoCabinetSerializer(read_only=True, many=True)

    class Meta:
        model = Cabinet
        fields = ['id', 'cabinet_name', 'uposition']
        depth = 2


class CabinetNodepthSerializer(serializers.ModelSerializer):
    """
    Cabinet序列化类
    No depth
    """

    class Meta:
        model = Cabinet
        fields = ['id', 'cabinet_name', 'idc']
        validators = [
            UniqueTogetherValidator(
                queryset=Cabinet.objects.all(),
                fields=('cabinet_name', 'idc'),
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
            cabinet_obj.uposition.create(u_name=i)


class IdcSerializer(serializers.ModelSerializer):
    """
    Idc序列化类
    """

    cabinet = CabinetSerializer(read_only=True, many=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建时间", help_text="创建时间", required=False,
                                            read_only=True)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="更新时间", help_text="更新时间", required=False,
                                            read_only=True)

    class Meta:
        model = Idc
        fields = ['id', 'idc_name', 'address', 'phone', 'remark', 'cabinet', 'create_date', 'update_date']
        depth = 2
