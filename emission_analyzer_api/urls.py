from django.urls import path
#importing the methods from views.py which are used to parse the json data and return the response
from .views import addUser, addEngine, getUser, getEngines
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-user/", addUser, name="add_user"),
    path("add-engine/", addEngine, name="add_engine"),
    path("get_user/<str:user_id>", getUser, name="get_user"),
    path("get-engines/<str:user_id>", getEngines, name="get_engines")
]