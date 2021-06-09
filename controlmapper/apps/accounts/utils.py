from .serializers import UserSerializer
from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    groups = [g.name for g in user.groups.all()]
    return {
        'username': user.username,
        'email': user.email,
        'groups': groups,
        'last_login': str(user.last_login),
        'failed_login': str(user.failed_login),
        'role': user.role.name if user.role else None,
        'is_superuser': user.is_superuser,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(datetime.utcnow().utctimetuple())
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Overriding default handler to include user information.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
