#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 16:08
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from rest_framework import serializers
from .models import Server, Nic, ServerIp
from manufactory.models import Manufactory, ProductModel


class ServerAutoSerializer(serializers.Serializer):
    """
    服务器自动采集序列化类
    """

    ip_managemant = serializers.IPAddressField(max_length=15, label="管理IP", help_text="管理IP")
    hostname = serializers.CharField(max_length=24, label="主机名", help_text="主机名")
    os_type = serializers.CharField(max_length=16, label="系统类型", help_text="系统类型")
    os_release = serializers.CharField(max_length=16, label="操作系统版本", help_text="操作系统版本")
    cpu_model = serializers.CharField(max_length=128, label="CPU型号", help_text="CPU型号")
    cpu_physics_count = serializers.IntegerField(label="物理CPU个数", help_text="物理CPU个数")
    cpu_core_count = serializers.IntegerField(label="CPU核数", help_text="CPU核数")
    cpu_logic_count = serializers.IntegerField(label="逻辑CPU个数", help_text="逻辑CPU个数")
    mem_capacity = serializers.DecimalField(max_digits=10, decimal_places=2, label="内存大小(GB)", help_text="内存大小(GB)")
    disk_capacity = serializers.DecimalField(max_digits=10, decimal_places=2, label="磁盘容量(GB)", help_text="磁盘容量(GB)")
    sn = serializers.CharField(max_length=128, label="序列号", help_text="序列号")
    uuid = serializers.CharField(max_length=128, label="UUID", help_text="UUID")
    productmodel = serializers.CharField(max_length=32, label="设备型号", help_text="设备型号")
    manufactory = serializers.CharField(max_length=64, label="制造商", help_text="制造商")
    net = serializers.JSONField(required=True, write_only=True)

    def validate_manufactory(self, value):
        try:
            return Manufactory.objects.get(manufactory_name__exact=value)
        except Manufactory.DoesNotExist:
            return self.create_manufactory(value)

    def validate(self, attrs):
        manufactory_obj = attrs["manufactory"]
        try:
            attrs["productmodel"] = manufactory_obj.productmodel_set.get(product_name__exact=attrs["productmodel"])
        except ProductModel.DoesNotExist:
            attrs["productmodel"] = self.create_productmodel(attrs["productmodel"], manufactory_obj)
        return attrs


    @staticmethod
    def create_manufactory(manufactory_name):
        return Manufactory.objects.create(manufactory_name=manufactory_name)

    @staticmethod
    def create_productmodel(product_name, manufactory):
        return ProductModel.objects.create(product_name=product_name, manufactory=manufactory)

    def create_server(self, validated_data):
        net = validated_data.pop("net")
        server_obj = Server.objects.create(**validated_data)
        self.check_nic(server_obj, net)
        return server_obj

    def update_server(self, instance, validated_data):
        instance.hostname = validated_data.get("hostname", instance.hostname)
        instance.os_type = validated_data.get("os_type", instance.os_type)
        instance.os_release = validated_data.get("os_release", instance.os_release)
        instance.cpu_model = validated_data.get("cpu_model", instance.cpu_model)
        instance.cpu_physics_count = validated_data.get("cpu_physics_count", instance.cpu_physics_count)
        instance.cpu_core_count = validated_data.get("cpu_core_count", instance.cpu_core_count)
        instance.cpu_logic_count = validated_data.get("cpu_logic_count", instance.cpu_logic_count)
        instance.mem_capacity = validated_data.get("mem_capacity", instance.mem_capacity)
        instance.disk_capacity = validated_data.get("disk_capacity", instance.disk_capacity)
        instance.save()
        self.check_nic(instance, validated_data["net"])
        return instance

    def create(self, validated_data):
        uuid = validated_data["uuid"].lower()
        try:
            server_obj = Server.objects.get(uuid__icontains=uuid)
            return self.update_server(server_obj, validated_data)
        except Server.DoesNotExist:
            return self.create_server(validated_data)

    def check_nic(self, server_obj, net):
        """
        判断服务器中是否有网卡设备
        """
        serverip_queryset = server_obj.nic_set.all()  # 获取该服务器对象的所有网卡
        post_nic_queryset = []
        for n in net:
            try:
                nic_obj = serverip_queryset.get(nic_name__exact=n['nic_name'])
                Nic.objects.filter(nic_name__exact=n['nic_name']).update(mac_address=n["mac_address"])  # 强制更新mac地址
                self.check_serverip(nic_obj, n["ip_addrs"])
            except Nic.DoesNotExist:
                ip_info = n.pop("ip_addrs")
                nic_obj = self.create_nic(n, server_obj)
                self.check_serverip(nic_obj, ip_info)
            post_nic_queryset.append(nic_obj)
        for nic_obj in set(serverip_queryset) - set(post_nic_queryset):  # 比对删除post之前的网卡信息
            nic_obj.delete()

    @staticmethod
    def create_nic(n, server_obj):
        """
        创建网卡设备
        """
        n["server"] = server_obj
        nic_obj = Nic.objects.create(**n)
        return nic_obj

    def check_serverip(self, nic_obj, ip_info):
        """
        判断服务器是否存在这个IP
        """
        serverip_queryset = nic_obj.serverip_set.all()  # 获取改网卡的所有IP
        post_serverip_queryset = []
        for ip in ip_info:
            try:
                serverip_obj = serverip_queryset.get(ip_addr__exact=ip['ip_addr'])
                ServerIp.objects.filter(ip_addr__exact=ip['ip_addr']).update(netmask=ip["netmask"])
            except ServerIp.DoesNotExist:
                serverip_obj = self.create_serverip(nic_obj, ip)
            post_serverip_queryset.append(serverip_obj)
        for serverip_obj in set(serverip_queryset) - set(post_serverip_queryset):
            print(serverip_obj)
            serverip_obj.delete()

    @staticmethod
    def create_serverip(nic_obj, ip):
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
