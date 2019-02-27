#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.routers import DefaultRouter
from .views import ManufactoryViewset,ProductModelViewset

manufactory_router = DefaultRouter()
manufactory_router.register("manufactory", ManufactoryViewset, base_name="manufactory")
manufactory_router.register("productmodel", ProductModelViewset, base_name="productmodel")