from rest_framework import viewsets
from .models import Idc, Cabinet
from .serializers import IdcSerializer, CabinetNodepthSerializer


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
    serializer_class = IdcSerializer

    def get_queryset(self):
        return Idc.objects.all()

    def list(self, request, *args, **kwargs):
        # 当传回status参数为1时，不分页

        nopage = request.query_params.get("nopage")
        supplier = self.get_queryset()
        if nopage == '1':
            self.paginator.page_size = supplier.count()
        page = self.paginate_queryset(supplier)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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


# class UpositionViewset(viewsets.ModelViewSet):
#     """
#     retrieve:
#         返回指定U位信息
#     list:
#         返回U位列表
#     update:
#         更新U位信息
#     partial_update:
#         更新部分U位字段
#     destory:
#         删除U位信息
#     create:
#         创建U位记录
#     """
#     queryset = Uposition.objects.all()
#     serializer_class = UpositionSerializer
