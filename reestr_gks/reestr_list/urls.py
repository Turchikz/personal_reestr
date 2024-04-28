from django.urls import path
from . import views
from .views import reestr_list, index, add_to_reestr

app_name = "reestr_list"

urlpatterns = [
    path("", index, name="index"),
    path("reestr/", reestr_list, name="reestr"),
    path("reestr/add/", add_to_reestr, name="additional"),
]
