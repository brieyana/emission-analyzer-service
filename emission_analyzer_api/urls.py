from django.urls import path
#importing the methods from views.py which are used to parse the json data and return the response
from .views import *

urlpatterns = [
    path("get_token", get_csrf_token, name="index"),
    path("add-user/", createUser, name="add_user"),
    path("add-engine/", addEngine, name="add_engine"),
    path("get_user/<str:user_id>", getUser, name="get_user"),
    path("get-engines/<str:user_id>", getEngines, name="get_engines"),
    path("predict_emissions", predictEmissions, name="predict_emissions"),
    path("edit_engine", editEngine, name="edit_engine"),
    path("get_engine_types", getEngineTypes, name="get_engine_types"),
    path("delete_engine/<str:user_id>/engines/<str:engine_id>", deleteEngine, name="delete_engine")
]