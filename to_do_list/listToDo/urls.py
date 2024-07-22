from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/login", views.pageInitSession, name="initSession"),
    path("users/register", views.pageRegister, name="register"),
    path("users/login", views.login, name="login"),
    path("users/logout", views.logout, name="logout"),
]