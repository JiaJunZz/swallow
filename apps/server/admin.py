from django.contrib import admin
from .models import Server, Nic, Driver

# Register your models here.

admin.site.register(Server)
admin.site.register(Nic)
admin.site.register(Driver)
