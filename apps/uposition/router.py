#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.routers import DefaultRouter
from .views import UpositionViewset

uposition_router = DefaultRouter()

uposition_router.register("uposition", UpositionViewset, base_name="uposition")
