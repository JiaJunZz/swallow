from rest_framework import viewsets
from .models import Idc,Cabinet
from .serializers import IdcSerializer,CabinetSerializer


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
    serializer_class = CabinetSerializer
