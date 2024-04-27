from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls, name='adminka'),
    path("", include("reestr_list.urls"), name='main'),
    
]
