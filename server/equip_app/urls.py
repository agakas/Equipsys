# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.AllUserViewSet)  #Все пользователи
router.register(r'organizations', views.AllOrganizationsViewSet) #Все организации
router.register(r'equipments', views.AllEquipmentsViewSet) #Всё оборудование

urlpatterns = [
    path('', include(router.urls)),
    path('current_user/', views.userView, name = 'user-list'), #получение текущего пользователя, походу это костыль
    #path('current_equipments/', views.equipmentsView, name = 'equipment-list'), #получение текущего пользователя, походу это костыль
]