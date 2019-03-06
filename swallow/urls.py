"""swallow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.authtoken import views
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from permcontrol.router import permcontrol_router
from supplier.router import supplier_router
from manufactory.router import manufactory_router
from server.router import server_router
from idc.router import idc_router
from cabinetunit.router import cabinetunit_router

route = DefaultRouter()

route.registry.extend(permcontrol_router.registry)
route.registry.extend(supplier_router.registry)
route.registry.extend(manufactory_router.registry)
route.registry.extend(server_router.registry)
route.registry.extend(idc_router.registry)
route.registry.extend(cabinetunit_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs", include_docs_urls("swallow运维平台API接口文档")),
    re_path(r"^api_auth",include("rest_framework.urls")),
    re_path(r"^", include(route.urls)),
    re_path(r'^api-token-auth/', views.obtain_auth_token)
]