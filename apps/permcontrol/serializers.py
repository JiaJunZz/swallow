#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 18:42
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "phone")

    def to_representation(self, instance):
        """
            序列化
            """
        ret = super(UserSerializer, self).to_representation(instance)
        group_queryset = instance.groups.all()
        group_list = []
        for group_obj in group_queryset:
            group_list.append({
                "id": group_obj.id,
                "name": group_obj.name
            })
        ret['groups'] = group_list
        return ret


class GroupsSerializer(serializers.ModelSerializer):
    """
    Groups序列化类
    """


    class Meta:
        model = Group
        fields = ("id", "name",)

    def to_representation(self, instance):
        """
            序列化
            """
        ret = super(GroupsSerializer, self).to_representation(instance)
        user_queryset = instance.user_set.all()
        user_list = []
        for user_obj in user_queryset:
            user_list.append({
                "id": user_obj.id,
                "username": user_obj.username,
                "name": user_obj.name,
                "email": user_obj.email,
                "phone": user_obj.phone,
            })
        ret['users'] = user_list
        return ret
