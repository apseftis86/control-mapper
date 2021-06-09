from django.contrib.auth import authenticate, user_logged_in
from .models import CustomUser
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class JWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)
            if user:
                if not user.is_active:
                    msg = 'User account is not active.'
                    raise serializers.ValidationError(msg)
                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                try:
                    user = CustomUser.objects.get(username=credentials['username'])
                    if user:
                        user.failed_login = datetime.now()
                        user.save()
                except ObjectDoesNotExist:
                    pass
                msg = 'Unable to log in using those credentials'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
