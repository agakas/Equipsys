from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer, OrganizationSerializer, EquipmentSerializer
from .models import User, Organization, Equipment
from .permissions import IsAuthOrAnyoneCanCreate  #создавать может кто угодно, а просматривать только админ
from rest_framework.permissions import IsAuthenticated, AllowAny


class AllUserViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthOrAnyoneCanCreate]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
  # УДАЛИТЬ
    def create(self, request, *args, **kwargs):
        response = super(AllUserViewSet, self).create(request, *args, **kwargs)
        return response
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

class EquipsOfOrg(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EquipmentSerializer
    def get_queryset(self):
        org = self.request.GET.get('org_id', None)
        return Equipment.objects.filter(organization=org)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def userView(request):
    permission_classes = [IsAuthenticated]
    serializer = UserSerializer(request.user)
    return JsonResponse(serializer.data)

def equipOfOrgView(request, id_org):
    #permission_classes = [IsAuthenticated]
    print(id_org)
    def get_queryset(self):
        return Equipment.objects.filter(organization=id_org)

#на удаление
@api_view(['POST'])
def login_user(request):
    permission_classes = [AllowAny]
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,  password=password)
    if user is not None:
       login(request, user)
       if request.user.is_superuser:
           #Если пользователь является админом, то это посылается в заголовке
           return HttpResponse("Admin Logged In", headers={'IsAdmin':True}, status=status.HTTP_200_OK)
       print('Крутяк')
       return HttpResponse("Logged In", status=status.HTTP_200_OK)
    print('Такое себе')
    return HttpResponse("Not Logged In", status=status.HTTP_400_BAD_REQUEST)

def unique_inn_org(request, inn):
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all().order_by('id')

    if queryset.filter(inn=inn).exists():
        return HttpResponse("It Exists", status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse("Exists", status=status.HTTP_200_OK)

def log_out(request):
    logout(request)

#def equipmentsView(request):
#    permission_classes = [IsAuthenticated]
#    pk = self.kwargs.get('pk')
#    serializer = EquipmentSerializer(organization)
#    return JsonResponse(serializer.data)