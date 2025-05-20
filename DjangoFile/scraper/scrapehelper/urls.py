from django.urls import path
from . import views, urls

urlpatterns = [
    path("", views.home, name='home'),
    # use query params to pass in variables
    path("get_data_json/", views.get_data_json, name = "get_data_json"),
]