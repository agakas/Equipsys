#from django.shortcuts import render
#from rest_framework import  status
#from rest_framework.response import Response
#from .models import User, Organization, Equipment

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.fields import CurrentUserDefault
from rest_framework.decorators import api_view

from .serializers import UserSerializer, OrganizationSerializer, EquipmentSerializer
from .models import User, Organization, Equipment
from .permissions import IsAdminOrAnyoneCanCreate  #создавать может кто угодно, а просматривать только админ
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#from rest_framework.decorators import api_view

class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAnyoneCanCreate]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
 #   http_method_names = ['get', 'post', 'put', 'patch', 'delete']

class AllOrganizationsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all().order_by('id')
    serializer_class = OrganizationSerializer

class AllEquipmentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Equipment.objects.all().order_by('id')
    serializer_class = EquipmentSerializer

class EquipmentsOfOrgViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        organ = self.kwargs['organization']
        return Equipment.objects.filter(organization=organ)

class OrganizationsOfUser(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    def get_queryset(self):
        user = self.request.user.id
        return Organization.objects.filter(users=user)

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def userView(request):
    permission_classes = [IsAuthenticated]
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data)

#def equipmentsView(request):
#    permission_classes = [IsAuthenticated]
#    pk = self.kwargs.get('pk')
#    serializer = EquipmentSerializer(organization)
#    return JsonResponse(serializer.data)