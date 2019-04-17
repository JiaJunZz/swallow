#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 18:42
# @Author  : ZJJ
# @Email   : 597105373@qq.com
from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    password = serializers.CharField(write_only=True,required=True,label="密码", help_text="密码")

    class Meta:
        model = User
        fields = ("id", "username", "name", "email", "phone", "password","is_superuser")

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

    def create(self, validated_data):
        user_obj = super(UserSerializer, self).create(validated_data)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return user_obj


class ChangeUserPasswdSerializer(serializers.Serializer):
    """
    更改用户密码序列化类
    """
    old_password = serializers.CharField(required=False,write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


class GroupsSerializer(serializers.ModelSerializer):
    """
    用户组序列化类
    """

    class Meta:
        model = Group
        fields = ("id", "name",)

    def to_representation(self, instance):
        """
            序列化
            """
        ret = super(GroupsSerializer, self).to_representation(instance)
        perm_queryset = instance.permissions.all()
        user_queryset = instance.user_set.all()
        user_list = []
        perm_list = []
        for perm_obj in perm_queryset:
            perm_list.append({
                "id": perm_obj.id,
                "codename": perm_obj.codename,
            })
        ret['perm'] = perm_list
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


class PermissionSerializer(serializers.ModelSerializer):
    """
    权限序列化类
    """

    class Meta:
        model = Permission
        fields = "__all__"
