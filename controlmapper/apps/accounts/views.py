# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from .serializers import RegistrationSerializer, UserDetailSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from .models import CustomUser
from rest_framework import exceptions
import logging


class RegistrationView(viewsets.ViewSet):
    model = None
    queryset = None
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger = logging.getLogger('user')
        request.data['username'] = request.data['username'].lower()
        user_data = self.serializer_class(data=request.data)
        if user_data.is_valid(raise_exception=True):
            user = user_data.get_cleaned_data()
            new_user = CustomUser.objects.create_user(**user)
            new_user.is_active = False
            new_user.save()
            logger.info(f'New user created: {new_user.get_name()}')
            return Response('Registration complete! Once your account is activated you will be able to sign in.')
        else:
            logger.error(f"Error while creating user {request.data['username']}")
            raise exceptions.NotAcceptable('User could not be created')


class LoginView:
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    serializer_detail_class = UserDetailSerializer

    @action(methods=['get'], detail=False)
    def current_profile(self, request):
        queryset = CustomUser.objects.get(id=request.user.pk)
        serializer = UserDetailSerializer(queryset, context={'groups': request.user.groups})
        return Response(serializer.data)
