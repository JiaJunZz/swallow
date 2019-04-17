from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import UserSerializer, GroupsSerializer, PermissionSerializer, ChangeUserPasswdSerializer
from .filter import UsersFilter, GroupsFilter

User = get_user_model()


class PersonalInfoViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
        返回登录用户信息
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


class ChangeUserPasswdView(viewsets.GenericViewSet,
                           mixins.UpdateModelMixin):
    """
    更新用户的密码
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = ChangeUserPasswdSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangeUserPasswdSerializer(self.object, data=request.data)
        change_user = User.objects.get(pk=kwargs['pk'])
        print(change_user)

        if serializer.is_valid():
            if self.object.is_superuser is True:
                print('sup')
                change_user.set_password(serializer.validated_data.get("new_password"))
            elif self.object.is_superuser is False and self.object == change_user:
                old_password = serializer.validated_data.get("old_password", [])
                if not change_user.check_password(old_password):
                    return Response("旧密码输入错误",
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    change_user.set_password(serializer.validated_data.get("new_password"))
            elif self.object.is_superuser is False and self.object != change_user:
                return Response("只允许管理员或所属用户修改",
                                status=status.HTTP_401_UNAUTHORIZED)
            change_user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
