from rest_framework import viewsets
from .models import Idc, Cabinet, Uposition
from .serializers import IdcSerializer, CabinetNodepthSerializer, UpositionSerializer


class IdcViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定Idc信息
    list:
        返回Idc列表
    update:
        更新Idc信息
    partial_update:
        更新部分Idc字段
    destory:
        删除Idc信息
    create:
        创建Idc记录
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer


class CabinetViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定机柜信息
    list:
        返回机柜列表
    update:
        更新机柜信息
    partial_update:
        更新部分机柜字段
    destory:
        删除机柜信息
    create:
        创建机柜记录
    """
    queryset = Cabinet.objects.all()
    serializer_class = CabinetNodepthSerializer


class UpositionViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定U位信息
    list:
        返回U位列表
    update:
        更新U位信息
    partial_update:
        更新部分U位字段
    destory:
        删除U位信息
    create:
        创建U位记录
    """
    queryset = Uposition.objects.all()
    serializer_class = UpositionSerializer
