# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
#router.register(r'user', views.UserViewSet)
router.register(r'users', views.AllUserViewSet)
router.register(r'organizations', views.AllOrganizationViewSet)
router.register(r'equipments', views.AllEquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]