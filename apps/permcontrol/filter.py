#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 15:49
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from django.contrib.auth.models import Group
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class GroupsFilter(filters.FilterSet):
    """
    用户组搜索类
    """
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Group
        fields = ["name"]


class UsersFilter(filters.FilterSet):
    keywords = filters.CharFilter(method="my_custom_filter")

    def my_custom_filter(self, queryset, name, value):
        # 对email,username,name进行模糊搜索
        return queryset.filter(
            Q(username__icontains=value) | Q(email__icontains=value)
            | Q(name__icontains=value))

    class Meta:
        model = User
        fields = ["keywords"]
