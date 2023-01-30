# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('login', views.sign_in_action),
    path('sign_up', views.sign_up),
    path('registration', views.sign_up_action),
    path('exit', views.log_out),
    path('main', views.home),
]