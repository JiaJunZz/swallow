from django.shortcuts import render
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer

# Create your views here.
class SupplierViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定制造商信息
    list:
        返回制造商列表
    update:
        更新制造商信息
    partial_update:
        更新部分制造商字段
    destory:
        删除制造商信息
    create:
        创建制造商记录
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
