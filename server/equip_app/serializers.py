from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from .models import User, Organization, Equipment
from django.contrib.auth import update_session_auth_hash


#Сделай раздельные сериализаторы чтобы при get не видеть кэш пароля
class UserSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    class Meta:
        model  = User
        fields = ("id" , "username", "password", "email", "created_at", "updated_at", "is_superuser")

        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password = make_password(validated_data['password'])
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.save()

            password = validated_data.get('password', None)
            if password:
                instance.set_password(password)
                instance.save()
            update_session_auth_hash(self.context.get('request'), instance)
            return instance

class UserForViewSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    class Meta:
        model  = User
        fields = ("id" , "username", "email", "created_at", "updated_at", "is_superuser")

class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    class Meta:
        model  = Organization
        fields = ("id" , "name", "inn", "created_at", "updated_at", "users")

    

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    #organization = serializers.IntegerField(source='organization.id')
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    class Meta:
        model  = Equipment
        fields = ("id" , "serial", "organization", "created_at", "updated_at")