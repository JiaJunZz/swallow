#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from idc.models import Cabinet
from server.models import Server
from .models import CabinetUnit




class CabinetUnitSerializer(serializers.Serializer):
    u_number = serializers.IntegerField(required=True, label="U位", help_text="U位")
    cabinet = serializers.PrimaryKeyRelatedField(many=False, queryset=Cabinet.objects.all(), label="所属机柜", help_text="所属机柜")
    server = serializers.PrimaryKeyRelatedField(many=False, queryset=Server.objects.all(), label="服务器", help_text="服务器")

    def to_representation(self, instance):
        """
        序列化
        """
        cabinet_obj = instance.cabinet
        server_obj = instance.server
        ret = super(CabinetUnitSerializer, self).to_representation(instance)
        ret["cabinet"] = {
            "cabinet_id": cabinet_obj.id,
            "cabinet_name": cabinet_obj.cabinet_name
        }
        ret["server"] = {
            "server_id": server_obj.id,
            "server_ip_managemant": server_obj.ip_managemant
        }
        return ret

    def to_internal_value(self, data):
        """
        反序列化验证后执行create方法
        """
        return super(CabinetUnitSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        return CabinetUnit.objects.create(**validated_data)


