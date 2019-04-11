#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/14 14:49
# @Author  : ZJJ
# @Email   : 597105373@qq.com

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
