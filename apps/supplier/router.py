#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.routers import DefaultRouter
from .views import SupplierViewset

supplier_router = DefaultRouter()
supplier_router.register("supplier", SupplierViewset, base_name="supplier")