from django.urls import path
from . import views
from .views import reestr_list, index, PostAddView, add_to_register


app_name = "reestr_list"

urlpatterns = [
    path("", index, name="index"),
    path("reestr/", reestr_list, name="reestr"),
    path("reestr/add/", add_to_register, name="add_to_register"),
    path("reestr/add_to/", PostAddView.as_view(), name="additional_fpp"),
]
