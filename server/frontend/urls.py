# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('sign_up', views.sign_up),
]