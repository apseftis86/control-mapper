from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'is_superuser')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'groups', 'last_login')


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)

    class Meta:
        model =  CustomUser
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def custom_signup(self, request, user):
        # Will need to save organization here
        pass
