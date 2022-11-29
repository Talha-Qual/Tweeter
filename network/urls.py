
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.login_register, name="login_register"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
