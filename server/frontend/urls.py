# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('login', views.sign_in_action),
    path('sign_up', views.sign_up),
    path('registration', views.sign_up_action),
    path('edit_current_user', views.edit_current_user),
    path('delete_current_user', views.delete_current_user),
    path('add_equip_of_org/<org_id>', views.add_equip_of_org),
    path('edit_equip/<equip_id>', views.edit_equip),
    path('del_equip/<equip_id>', views.del_equip),
    path('user_to_admin/<user_id>', views.user_to_admin),
    path('delete_user_id/<user_id>', views.delete_user_id),
    path('edit_form_org/<org_id>', views.edit_org),
    path('delete_org/<org_id>', views.delete_org),
    path('exit', views.log_out),
    path('main', views.home),
]