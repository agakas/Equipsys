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
    path('current_user/', views.userView, name = 'current_user-details'), #получение текущего пользователя, походу это костыль
    path('current_equipments/organization/<int:organization>', views.EquipmentsOfOrgViewSet.as_view({'get':'list'}), name = 'current_equipment-list'), #получаем всё оборудование определённой организации
    path('current_organizations/', views.OrganizationsOfUser.as_view({'get':'list'}), name = 'current_organization-list'),

    path('login_user/', views.login_user),
    path('logout_user/', views.log_out)
]