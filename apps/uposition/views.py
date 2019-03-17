from django.shortcuts import render
from rest_framework import viewsets
from .models import Uposition
from .serializers import UpositionSerializer

# Create your views here.

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