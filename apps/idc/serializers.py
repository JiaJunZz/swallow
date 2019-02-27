#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from .models import Idc,Cabinet
from rest_framework.validators import UniqueValidator


class IdcSerializer(serializers.Serializer):
    """
    Idc序列化类
    """
    id = serializers.IntegerField(read_only=True)
    idc_name = serializers.CharField(required=True, max_length=16, label="机房名称", help_text="机房名称",
                                     validators=[UniqueValidator(queryset=Idc.objects.all(), message="该机房已存在")])
    address = serializers.CharField(allow_blank=True, max_length=128, label="机房地址", help_text="机房地址")
    phone = serializers.CharField(allow_blank=True, max_length=16, label="机房电话", help_text="机房电话")
    remark = serializers.CharField(allow_blank=True, max_length=255, label="备注", help_text="备注")

    def create(self, validated_data):
        return Idc.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idc_name = validated_data.get("idc_name", instance.idc_name)
        instance.address = validated_data.get("address", instance.address)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.remark = validated_data.get("remark", instance.remark)
        instance.save()
        return instance


class CabinetSerializer(serializers.Serializer):
    idc = serializers.PrimaryKeyRelatedField(many=False, queryset=Idc.objects.all(), label="所属机房", help_text="所属机房")
    cabinet_name = serializers.CharField(required=True, label="机柜号", help_text="机柜号")

    def to_representation(self, instance):
        """
        序列化
        """
        idc_obj = instance.idc
        ret = super(CabinetSerializer, self).to_representation(instance)
        ret["idc"] = {
            "id": idc_obj.id,
            "idc_name": idc_obj.idc_name
        }
        return ret

    def to_internal_value(self, data):
        """
        反序列化验证后执行create方法
        """
        return super(CabinetSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        return Cabinet.objects.create(**validated_data)

    def validate(self, attrs):
        idc_obj = attrs["idc"]
        cabinet_name = attrs["cabinet_name"]
        try:
            idc_obj.cabinet_set.get(cabinet_name__exact=cabinet_name)
            raise serializers.ValidationError("此机柜号存在")
        except Cabinet.DoesNotExist:
            return attrs
