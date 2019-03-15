from django.shortcuts import render
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework.response import Response
from core.pagination import StandardResultsSetPagination

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
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.all()

    def list(self, request, *args, **kwargs):

        status = request.query_params.get("status")
        supplier = self.get_queryset()
        if status == '1':
            self.paginator.page_size = supplier.count()

        page = self.paginate_queryset(supplier)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)