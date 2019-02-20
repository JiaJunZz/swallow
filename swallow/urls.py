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
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from idc.views import IdcViewset,CabinetViewset
from users.views import UserViewset
from manufactory.views import ManufactoryViewset, ProductModelViewset
from supplier.views import SupplierViewset
from server.views import ServerAutoViewset,NicViewset,ServerIpViewset,ServerViewset
from cabinetunit.views import CabinetUnitViewset

route = DefaultRouter()
route.register("idc", IdcViewset, base_name="idc")
route.register("cabinet", CabinetViewset, base_name="cabinet")
route.register("cabinetunit", CabinetUnitViewset, base_name="cabinetunit    ")
route.register("users", UserViewset, base_name="users")
route.register("manufactory", ManufactoryViewset, base_name="manufactory")
route.register("productmodel", ProductModelViewset, base_name="productmodel")
route.register("suppliertmodel", SupplierViewset, base_name="suppliertmodel")
route.register("serverAuto", ServerAutoViewset, base_name="serverAuto")
route.register("server", ServerViewset, base_name="server")
route.register("nic", NicViewset, base_name="nic")
route.register("serverip", ServerIpViewset, base_name="serverip")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs", include_docs_urls("swallow运维平台API接口文档")),
    re_path(r"^api_auth",include("rest_framework.urls")),
    re_path(r"^", include(route.urls))
]
