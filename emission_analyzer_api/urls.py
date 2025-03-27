from django.urls import path
from .views import addUser, addEngine #importing the methods from views.py which are used to parse the json data and return the response

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-user/", addUser, name="add_user"),
    path("add-engine/", addEngine, name="add_engine")
]