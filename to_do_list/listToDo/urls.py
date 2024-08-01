from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/login", views.login, name="initSession"),
    path("users/register", views.register, name="register"),
    path("users/login", views.login, name="login"),
    path("users/logout", views.logout, name="logout"),
    path("task/create",views.createTask, name="Create"),
    path("task/delete/<int:id>",views.deleteTask, name="Delete"),
    path("task/update/<int:id>",views.updateTask, name="Update"),
    path("task/list",views.listTask, name="List"),
]