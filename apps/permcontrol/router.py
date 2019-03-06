#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 14:14
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from .views import UserViewset,GroupsViewset,UserGroupViewset
from rest_framework.routers import DefaultRouter

permcontrol_router = DefaultRouter()
permcontrol_router.register("users", UserViewset, base_name="users")
permcontrol_router.register("groups", GroupsViewset, base_name="groups")
permcontrol_router.register("usergroup", UserGroupViewset, base_name="usergroup")