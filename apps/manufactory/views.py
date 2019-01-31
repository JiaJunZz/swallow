from rest_framework import viewsets
from .models import Manufactory, ProductModel
from .serializers import ManufactorySerializer, ProductModelSerializer


# Create your views here.

class ManufactoryViewset(viewsets.ModelViewSet):
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
    queryset = Manufactory.objects.all()
    serializer_class = ManufactorySerializer


class ProductModelViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定产品型号信息
    list:
        返回产品型号列表
    update:
        更新产品型号信息
    partial_update:
        更新部分产品型号字段
    destory:
        删除产品型号信息
    create:
        创建产品型号记录
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
