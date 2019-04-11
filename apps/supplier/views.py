from rest_framework import viewsets
from rest_framework.response import Response
from .models import Supplier
from .serializers import SupplierSerializer


# Create your views here.
class SupplierViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定供应商信息
    list:
        返回供应商列表
    update:
        更新供应商信息
    partial_update:
        更新部分供应商字段
    destory:
        删除供应商息
    create:
        创建供应商记录
    """

    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.all()

    def list(self, request, *args, **kwargs):
        # 当传回nopage参数为1时，不分页
        queryset = self.filter_queryset(self.get_queryset())
        nopage = request.query_params.get("nopage")
        supplier = self.get_queryset()
        if nopage == '1':
            self.paginator.page_size = supplier.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)