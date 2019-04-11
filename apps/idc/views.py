from rest_framework import viewsets
from rest_framework.response import Response
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
        # 当传回nopage参数为1时，不分页
        queryset = self.filter_queryset(self.get_queryset())
        nopage = request.query_params.get("nopage")
        idc = self.get_queryset()
        if nopage == '1':
            self.paginator.page_size = idc.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

    serializer_class = CabinetNodepthSerializer

    def get_queryset(self):
        return Cabinet.objects.all()

    def list(self, request, *args, **kwargs):
        # 当传回nopage参数为1时，不分页
        queryset = self.filter_queryset(self.get_queryset())
        nopage = request.query_params.get("nopage")
        cabinet = self.get_queryset()
        if nopage == '1':
            self.paginator.page_size = cabinet.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)