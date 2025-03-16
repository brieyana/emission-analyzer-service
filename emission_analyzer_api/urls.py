from django.urls import path
from .views import addUser

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-user/", addUser, name="add_user")
]