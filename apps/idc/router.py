#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.routers import DefaultRouter
from .views import CabinetViewset, IdcViewset, UpositionViewset

idc_router = DefaultRouter()
idc_router.register("idc", IdcViewset, base_name="idc")
idc_router.register("cabinet", CabinetViewset, base_name="cabinet")
idc_router.register("uposition", UpositionViewset, base_name="uposition")
