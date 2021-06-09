from rest_framework_jwt.views import ObtainJSONWebToken

from .util_serializer import JWTSerializer
# Create your views here.


class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer