#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 16:08
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from rest_framework import serializers
from .models import Server, Nic, ServerIp, Cpu
from manufactory.models import Manufactory,ProductModel


class ServerAutoSerializer(serializers.Serializer):
    """
    服务器自动采集序列化类
    """

    ip_managemant = serializers.IPAddressField(max_length=15,label="管理IP",help_text="管理IP")
    hostname = serializers.CharField(max_length=24,label="主机名",help_text="主机名")
    os_type = serializers.CharField(max_length=16,label="系统类型", help_text="系统类型")
    os_release = serializers.CharField(max_length=16, label="操作系统版本",help_text="操作系统版本")
    mem_capacity = serializers.DecimalField(max_digits=10, decimal_places=2, label="内存大小(GB)",help_text="内存大小(GB)")
    disk_capacity = serializers.DecimalField(max_digits=10, decimal_places=2,label="磁盘容量(GB)",help_text="磁盘容量(GB)")
    sn = serializers.CharField(max_length=32,label="序列号", help_text="序列号")
    uuid = serializers.CharField(max_length=64,label="UUID",help_text="UUID")
    productmodel = serializers.CharField(max_length=32,label="设备型号",help_text="设备型号")
    manufactory = serializers.CharField(max_length=64,label="制造商",help_text="制造商")
    net = serializers.JSONField(required=True,write_only=True)

    def validate_manufactory(self,value):
        try:
            return Manufactory.objects.get(manufactory_name__exact=value)
        except Manufactory.DoesNotExist:
            return self.create_manufactory(value)

    def validate(self, attrs):
        print(attrs)
        manufactory_obj = attrs["manufactory"]
        try:
            attrs["productmodel"] = manufactory_obj.productmodel_set.get(product_name__exact=attrs["productmodel"])
        except ProductModel.DoesNotExist:
            attrs["productmodel"] = self.create_productmodel(attrs["productmodel"],manufactory_obj)
        return attrs

    def create_manufactory(self, manufactory_name):
        return Manufactory.objects.create(manufactory_name=manufactory_name)


    def create_productmodel(self,product_name,manufactory):
        return ProductModel.objects.create(product_name=product_name,manufactory=manufactory)

    def create(self, validated_data):
        net = validated_data.pop("net")
        server_obj = Server.objects.create(**validated_data)
        self.check_nic(server_obj,net)
        return server_obj

    def check_nic(self,server_obj, net):
        for n in net:
          try:
              nic_obj = server_obj.nic_set.get(nic_name__exact=n['nic_name'])
          except Nic.DoesNotExist:
              self.create_nic(n,server_obj)

    def create_nic(self,n,server_obj):
        ip_addrs = n.pop("ip_addrs")
        n["server"] = server_obj
        nic_obj = Nic.objects.create(**n)
        self.check_serverip(nic_obj,ip_addrs)
        return nic_obj

    def check_serverip(self,nic_obj,ip_addrs):
        for ip in ip_addrs:
            try:
                ip_obj = nic_obj.serverip_set.get(ip_addr__exact=ip['ip_addr'])
            except ServerIp.DoesNotExist:
                self.create_serverip(nic_obj,ip)

    def create_serverip(self,nic_obj,ip):
        ip["nic"] = nic_obj
        serverip_obj = ServerIp.objects.create(**ip)
        return serverip_obj




class ServerSerializer(serializers.ModelSerializer):
    """
    网卡序列化类
    """

    class Meta:
        model = Server
        fields = "__all__"

class NicSerializer(serializers.ModelSerializer):
    """
    网卡序列化类
    """

    class Meta:
        model = Nic
        fields = "__all__"


class ServerIpSerializer(serializers.ModelSerializer):
    """
    IP地址序列化类
    """

    class Meta:
        model = ServerIp
        fields = "__all__"

class CpuSerializer(serializers.ModelSerializer):
    """
    Cpu序列化类
    """
    class Meta:
        model = Cpu
        fields = "__all__"
