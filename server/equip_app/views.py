#from django.shortcuts import render
#from rest_framework import  status
#from rest_framework.response import Response
#from rest_framework.decorators import api_view
#from .models import User, Organization, Equipment
from rest_framework import viewsets
from .serializers import UserSerializer, OrganizationSerializer, EquipmentSerializer
from .models import User, Organization, Equipment
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view

class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    #user_id = request.user.id
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class AllOrganizationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer

class AllEquipmentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Equipment.objects.all().order_by('id')
    serializer_class = EquipmentSerializer