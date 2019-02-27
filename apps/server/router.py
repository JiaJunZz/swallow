#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.routers import DefaultRouter
from .views import ServerAutoViewset,ServerViewset,NicViewset,ServerIpViewset

server_router = DefaultRouter()
server_router.register("serverauto", ServerAutoViewset, base_name="serverauto")
server_router.register("server", ServerViewset, base_name="server")
server_router.register("nic", NicViewset, base_name="nic")
server_router.register("serverip", ServerIpViewset, base_name="serverip")