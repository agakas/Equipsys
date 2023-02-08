# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('login', views.sign_in_action),
    path('sign_up', views.sign_up),
    path('registration', views.sign_up_action),
    path('delete_current_user', views.delete_current_user),
    path('add_equip_of_org/<org_id>', views.add_equip_of_org),
    path('del_equip/<equip_id>', views.del_equip),
    path('exit', views.log_out),
    path('main', views.home),
]