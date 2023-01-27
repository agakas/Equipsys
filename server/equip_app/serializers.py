from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from .models import User, Organization, Equipment


#Сделай раздельные сериализаторы чтобы при get не видеть ъэш пароля
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = User
        fields = ("id" , "username", "password", "email", "created_at", "updated_at")
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password = make_password(validated_data['password'])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserForViewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = User
        fields = ("id" , "username", "email", "created_at", "updated_at")

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model  = Organization
        fields = ("id" , "name", "inn", "created_at", "updated_at", "users")

    

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    #organization = serializers.IntegerField(source='organization.id')
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    class Meta:
        model  = Equipment
        fields = ("id" , "serial", "organization", "created_at", "updated_at")