from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions
from .serializers import UserSerializer, GroupsSerializer, PermissionSerializer
from .filter import UsersFilter, GroupsFilter

User = get_user_model()


class UserViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户信息
    list:
        返回用户列表
    update:
        更新用户信息
    partial_update:
        更新部分用户字段
    destory:
        删除用户信息
    create:
        创建用户记录
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_class = UsersFilter
    filter_fields = ("username", "email", "name")


class UserGroupViewset(viewsets.GenericViewSet,
                       mixins.UpdateModelMixin):
    """
    update:
        更新用户的用户组信息
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        user_obj.groups.set(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupsViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户组信息
    list:
        返回用户组列表
    update:
        更新用户组信息
    partial_update:
        更新部分用户组字段
    destory:
        删除用户组信息
    create:
        创建用户组记录
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupsSerializer
    filter_class = GroupsFilter
    filter_fields = ("name",)


class GroupMemberViewset(viewsets.GenericViewSet,
                         mixins.DestroyModelMixin):
    """
    destory:
        删除用户组中的成员信息
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupsSerializer

    def destroy(self, request, *args, **kwargs):
        group_obj = self.get_object()
        user_obj = User.objects.get(id=request.data['id'])
        user_obj.groups.remove(group_obj.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回权限信息
    list:
        返回权限列表
    """
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    pagination_class = None


class GroupPermViewset(viewsets.ModelViewSet):
    """
    partial_update:
        更新部分用户组字段
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupsSerializer

    def update(self, request, *args, **kwargs):
        group_obj = self.get_object()
        group_obj.permissions.set(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
