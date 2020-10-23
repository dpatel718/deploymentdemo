from ExamApp.views import mainpage
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index),
    path("mainpage", views.mainpage),
    path("register", views.register),
    path("login", views.login),
    path("travels", views.travels),
    path("logout", views.logout),
    path("travels/add", views.addTravel),
    path("add", views.add),
    path("travels/destination/<int:favId>", views.destination),
    path("favoriteItem/<int:favId>", views.favoriteItem)
]
