# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'organization', views.OrganizationViewSet)
router.register(r'equipment', views.EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]