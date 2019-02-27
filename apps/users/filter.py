#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 15:49
# @Author  : ZJJ
# @Email   : 597105373@qq.com


from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()



class UsersFilter(filters.FilterSet):
    username_email = filters.CharFilter(method="my_custom_filter")

    def my_custom_filter(self, queryset, name, value):
        # 对email,username进行模糊搜索
        return queryset.filter(
            Q(username__icontains=value) | Q(email__icontains=value))

    class Meta:
        model = User
        fields = ["username_email"]