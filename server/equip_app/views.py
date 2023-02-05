from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from .serializers import UserSerializer, OrganizationSerializer, EquipmentSerializer
from .models import User, Organization, Equipment
from .permissions import IsAdminOrAnyoneCanCreate  #создавать может кто угодно, а просматривать только админ
from rest_framework.permissions import IsAuthenticated, AllowAny


class AllUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAnyoneCanCreate]
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
  # УДАЛИТЬ
    def create(self, request, *args, **kwargs):
        response = super(AllUserViewSet, self).create(request, *args, **kwargs)
        return response
  #      return redirect('/api/frontend/') #нужно возвращать код ответа
  #  http_method_names = ['get', 'post', 'put', 'patch', 'delete']

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
       return HttpResponse("Logged In", headers={'IsAdmin':False}, status=status.HTTP_200_OK)
    print('Такое себе')
    return HttpResponse("Not Logged In", status=status.HTTP_400_BAD_REQUEST)

def log_out(request):
    logout(request)
    return HttpResponse("Logged Out", status=status.HTTP_200_OK)
#def equipmentsView(request):
#    permission_classes = [IsAuthenticated]
#    pk = self.kwargs.get('pk')
#    serializer = EquipmentSerializer(organization)
#    return JsonResponse(serializer.data)