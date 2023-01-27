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

class AllOrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer

class AllEquipmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Equipment.objects.all().order_by('id')
    serializer_class = EquipmentSerializer