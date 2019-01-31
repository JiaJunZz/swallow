from rest_framework import viewsets
from .models import Server, Nic, ServerIp,Cpu
from .serializers import ServerAutoSerializer, NicSerializer,ServerIpSerializer,CpuSerializer,ServerSerializer
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

class ServerViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回服务器信息
    list:
        返回服务器列表

    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class NicViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回网卡信息
    list:
        返回网卡列表
    """
    queryset = Nic.objects.all()
    serializer_class = NicSerializer

class ServerIpViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回Ip地址信息
    list:
        返回Ip地址列表
    """
    queryset = ServerIp.objects.all()
    serializer_class = ServerIpSerializer

class CpuViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回Cpu信息
    list:
        返回Cpu列表
    """
    queryset = Cpu.objects.all()
    serializer_class = CpuSerializer