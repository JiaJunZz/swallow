from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from .serializers import UserSerializer
from .filter import UsersFilter

# Create your views here.

User = get_user_model()


class UserViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定用户信息
    list:
        返回用户列表
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    # authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_class = UsersFilter
    filter_fields = ("username","email")
