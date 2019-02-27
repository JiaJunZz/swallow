from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializers import GroupsSerializer
from .filter import GroupsFilter
# Create your views here.

class GroupsViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupsSerializer
    filter_class = GroupsFilter
    filter_fields = ("name",)