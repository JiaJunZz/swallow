#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 16:08
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from rest_framework import serializers
from .models import Server, Nic,Driver
from manufactory.models import Manufactory, ProductModel
from uposition.models import Uposition


class ServerAutoSerializer(serializers.Serializer):
    """
    服务器自动采集序列化类
    """
    id = serializers.IntegerField(read_only=True)
    ip_managemant = serializers.IPAddressField(max_length=15, label="管理IP", help_text="管理IP")
    hostname = serializers.CharField(max_length=24, label="主机名", help_text="主机名")
    os_type = serializers.CharField(max_length=16, label="系统类型", help_text="系统类型")
    os_release = serializers.CharField(max_length=16, label="操作系统版本", help_text="操作系统版本")
    cpu_model = serializers.CharField(max_length=128, label="CPU型号", help_text="CPU型号")
    cpu_physics_count = serializers.IntegerField(label="物理CPU个数", help_text="物理CPU个数")
    cpu_core_count = serializers.IntegerField(label="CPU核数", help_text="CPU核数")
    cpu_logic_count = serializers.IntegerField(label="逻辑CPU个数", help_text="逻辑CPU个数")
    mem_capacity = serializers.DecimalField(max_digits=10, decimal_places=2, label="内存大小(GB)", help_text="内存大小(GB)")
    sn = serializers.CharField(max_length=128, label="序列号", help_text="序列号")
    uuid = serializers.CharField(max_length=128, label="UUID", help_text="UUID")
    productmodel = serializers.CharField(max_length=32, label="设备型号", help_text="设备型号")
    manufactory = serializers.CharField(max_length=64, label="品牌", help_text="品牌")
    nic = serializers.JSONField(required=True, write_only=True)
    driver = serializers.JSONField(required=True, write_only=True)


    def check_nic(self, server_obj, nic_list):
        """
        判断服务器中是否有网卡设备
        """
        nic_queryset = server_obj.nic_set.all()  # 获取该服务器对象的所有网卡
        post_nic_queryset = []
        for n in nic_list:
            try:
                nic_obj = nic_queryset.get(nic_name__exact=n['nic_name'])
                # 强制更新
                Nic.objects.filter(nic_name__exact=n['nic_name']).update(mac_address=n["mac_address"],
                                                                         ip_addr=n["ip_addr"], netmask=n["netmask"])
            except Nic.DoesNotExist:
                nic_obj = self.create_nic(n, server_obj)
            post_nic_queryset.append(nic_obj)
        for nic_obj in set(nic_queryset) - set(post_nic_queryset):  # 比对删除post之前的网卡信息
            nic_obj.delete()

    def check_driver(self, server_obj, driver_list):
        """
        判断服务器中是否有硬盘
        """
        driver_queryset = server_obj.driver_set.all()  # 获取该服务器对象的所有网卡
        post_driver_queryset = []
        for d in driver_list:
            try:
                driver_obj = driver_queryset.get(driver_name__exact=d['driver_name'])
                # 强制更新
                Driver.objects.filter(driver_name__exact=d['driver_name']).update(capacity=d["capacity"])
            except Driver.DoesNotExist:
                driver_obj = self.create_driver(d, server_obj)
            post_driver_queryset.append(driver_obj)
        for driver_obj in set(driver_queryset) - set(post_driver_queryset):  # 比对删除post之前的网卡信息
            driver_obj.delete()

    @staticmethod
    def create_nic(n, server_obj):
        """
        创建网卡设备
        """
        n["server"] = server_obj
        nic_obj = Nic.objects.create(**n)
        return nic_obj

    @staticmethod
    def create_driver(d, server_obj):
        """
        创建硬盘设备
        """
        d["server"] = server_obj
        print(d)
        Driver_obj = Driver.objects.create(**d)
        return Driver_obj

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
        nic_list = validated_data.pop("nic")
        driver_list = validated_data.pop("driver")
        server_obj = Server.objects.create(**validated_data)
        self.check_nic(server_obj, nic_list)
        self.check_driver(server_obj,driver_list)
        return server_obj

    def update(self, instance, validated_data):
        instance.ip_managemant = validated_data.get("ip_managemant", instance.ip_managemant)
        instance.hostname = validated_data.get("hostname", instance.hostname)
        instance.os_type = validated_data.get("os_type", instance.os_type)
        instance.os_release = validated_data.get("os_release", instance.os_release)
        instance.cpu_model = validated_data.get("cpu_model", instance.cpu_model)
        instance.cpu_physics_count = validated_data.get("cpu_physics_count", instance.cpu_physics_count)
        instance.cpu_core_count = validated_data.get("cpu_core_count", instance.cpu_core_count)
        instance.cpu_logic_count = validated_data.get("cpu_logic_count", instance.cpu_logic_count)
        instance.mem_capacity = validated_data.get("mem_capacity", instance.mem_capacity)
        instance.manufactory = validated_data.get("manufactory", instance.manufactory)
        instance.productmodel = validated_data.get("productmodel", instance.productmodel)
        validated_nic = validated_data.get("nic", [])
        self.check_nic(instance, validated_nic)
        validated_driver = validated_data.get("driver", [])
        self.check_driver(instance,validated_driver)
        instance.save()
        return instance

    def create(self, validated_data):
        uuid = validated_data["uuid"].lower()
        try:
            server_obj = Server.objects.get(uuid__icontains=uuid)
            return self.update(server_obj, validated_data)
        except Server.DoesNotExist:
            return self.create_server(validated_data)


class NicSerializer(serializers.ModelSerializer):
    """
    网卡序列化类
    """

    class Meta:
        model = Nic
        fields = "__all__"

class DriverSerializer(serializers.ModelSerializer):
    """
    硬盘序列化类
    """

    class Meta:
        model = Driver
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """
    服务器序列化类
    """
    productmodel = serializers.PrimaryKeyRelatedField(read_only=True)
    manufactory = serializers.PrimaryKeyRelatedField(read_only=True)
    uposition = serializers.JSONField(write_only=True,required=False,label="U位",help_text="U位")
    approach_date = serializers.DateField(required=False, label="进场日期",help_text="进场日期")
    expire_date = serializers.DateField(  required=False,label="过保日期",help_text="过保日期")
    create_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="创建时间", help_text="创建时间", required=False,
                                            read_only=True)
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", label="更新时间", help_text="更新时间", required=False,
                                            read_only=True)

    class Meta:
        model = Server
        fields = ['id','ip_managemant', 'hostname', 'os_type', 'os_release', 'cpu_model', 'cpu_physics_count',
                  'cpu_core_count', 'cpu_logic_count', 'mem_capacity', 'sn', 'uuid', 'productmodel',
                  'manufactory', 'supplier', 'remark', 'approach_date', 'expire_date', 'create_date', 'update_date','idc','cabinet',
                  'uposition']


    @staticmethod
    def relate_uposition(server_obj, uposition_data):
        """
        更新关联U位
        """
        u_list = []
        for u in uposition_data:
            u_obj = Uposition.objects.get(id=u)
            u_list.append(u_obj)
        server_obj.u_server.set(u_list)

    def create(self, validated_data):
        print(validated_data)
        try:
            uposition_data = validated_data.pop('uposition')
            # cabinet_id = validated_data.pop()
            server_obj = Server.objects.create(**validated_data)
            self.relate_uposition(server_obj, uposition_data)
        except:
            server_obj = Server.objects.create(**validated_data)
        return server_obj

    def update(self, instance, validated_data):
        instance.remark = validated_data.get("remark", instance.remark)
        instance.approach_date = validated_data.get("approach_date", instance.approach_date)
        instance.expire_date = validated_data.get("expire_date", instance.expire_date)
        instance.supplier = validated_data.get("supplier", instance.supplier)
        instance.idc = validated_data.get("idc", instance.idc)
        instance.cabinet = validated_data.get("cabinet", instance.cabinet)
        try:
            uposition_data = validated_data.get("uposition", [])
            self.relate_uposition(instance, uposition_data)
            instance.save()
        except:
            instance.save()
        return instance

    def to_representation(self, instance):
        supplier_obj = instance.supplier
        manufactory_obj = instance.manufactory
        productmodel_obj = instance.productmodel
        idc_obj = instance.idc
        cabinet_obj = instance.cabinet
        nic_queryset = instance.nic_set.all()
        driver_queryset = instance.driver_set.all()
        cabinet_unit_queryset = instance.u_server.all()
        ret = super(ServerSerializer, self).to_representation(instance)
        nic_list = []
        u_list = []
        dirver_list = []

        for nic_obj in nic_queryset:
            nic_list.append({
                "nic_id": nic_obj.id,
                "nic_name": nic_obj.nic_name,
                "mac_address": nic_obj.mac_address,
                "ip_addr": nic_obj.ip_addr,
                "netmask": nic_obj.netmask,
            })
        ret["nic"] = nic_list
        for driver_obj in driver_queryset:
            dirver_list.append({
                "driver_id": driver_obj.id,
                "driver_name": driver_obj.driver_name,
                "capacity": driver_obj.capacity,
            })
        ret["dirver"] = dirver_list
        if supplier_obj:
            ret["supplier"] = {
                "supplier_id": supplier_obj.id,
                "supplier_name": supplier_obj.supplier_name,
            }
        if idc_obj:
            ret["idc"] = {
                "idc_id": idc_obj.id,
                "idc_name": idc_obj.name,
            }
        if cabinet_obj:
            ret["cabinet"] = {
                "cabinet_id": cabinet_obj.id,
                "cabinet_name": cabinet_obj.name,
            }
        if manufactory_obj:
            ret["manufactory"] = {
                "manufactory_id": manufactory_obj.id,
                "manufactory_name": manufactory_obj.manufactory_name,
            }
        if productmodel_obj:
            ret["productmodel"] = {
                "productmodel_id": productmodel_obj.id,
                "productmodel_name": productmodel_obj.product_name,
            }

        for u_obj in cabinet_unit_queryset:
            u_list.append({
                "u_id": u_obj.id,
                "name": u_obj.name
            })
        ret["uposition"] = u_list
        return ret
