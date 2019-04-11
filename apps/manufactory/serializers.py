#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 18:58
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework import serializers
from .models import Manufactory, ProductModel


class ManufactorySerializer(serializers.ModelSerializer):
    """
    制造商序列化类
    """

    class Meta:
        model = Manufactory
        fields = "__all__"


class ProductModelSerializer(serializers.ModelSerializer):
    """
    产品型号序列化类
    """

    class Meta:
        model = ProductModel
        fields = "__all__"

    def validate(self, attrs):
        manufactory_obj = attrs["manufactory"]
        product_name = attrs["product_name"]
        try:
            manufactory_obj.productmodel_set.get(product_name__exact=product_name)
            raise serializers.ValidationError("此型号存在")
        except ProductModel.DoesNotExist:
            return attrs

    def to_representation(self, instance):
        manufactory = instance.manufactory
        ret = super(ProductModelSerializer, self).to_representation(instance)
        ret["manufactory"] = {
            "id": manufactory.id,
            "name": manufactory.manufactory_name
        }
        return ret
