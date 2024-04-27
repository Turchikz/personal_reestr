from django.urls import path
from . import views
from .views import reestr_list, index

app_name = "reestr_list"

urlpatterns = [
    path("", index, name="index"),
    path("reestr/", reestr_list, name="reestr"),
]
