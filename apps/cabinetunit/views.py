from django.shortcuts import render

from rest_framework import viewsets
from .models import CabinetUnit
from .serializers import CabinetUnitSerializer

# Create your views here.
class CabinetUnitViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定机柜U位信息
    list:
        返回机柜U位列表
    update:
        更新机柜U位信息
    partial_update:
        更新部分机柜U位字段
    destory:
        删除机柜U位信息
    create:
        创建机柜U位记录
    """
    queryset = CabinetUnit.objects.all()
    serializer_class = CabinetUnitSerializer