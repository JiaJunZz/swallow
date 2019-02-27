#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 15:49
# @Author  : ZJJ
# @Email   : 597105373@qq.com


from django_filters import rest_framework as filters
from django.contrib.auth.models import Group


class GroupsFilter(filters.FilterSet):
    """
    用户组搜索类
    """
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Group
        fields = ["name"]
