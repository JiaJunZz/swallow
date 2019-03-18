from rest_framework import viewsets
from .models import Server, Nic
from .serializers import ServerAutoSerializer, NicSerializer, ServerSerializer
from .filter import ServerFilter


# Create your views here.

class ServerAutoViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回服务器信息
    list:
        返回服务器列表
    update:
        更新服务器信息
    partial_update:
        更新部分服务器字段
    destory:
        删除服务器信息
    create:
        创建服务器记录
    """
    queryset = Server.objects.all()
    serializer_class = ServerAutoSerializer


class ServerViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回服务器信息
    list:
        返回服务器列表
    update:
        更新服务器信息
    partial_update:
        更新部分服务器字段
    destory:
        删除服务器信息
    create:
        创建服务器记录
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter


class NicViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回网卡信息
    list:
        返回网卡列表
    """
    queryset = Nic.objects.all()
    serializer_class = NicSerializer
