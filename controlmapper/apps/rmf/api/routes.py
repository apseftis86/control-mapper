from rest_framework import routers
from .v1 import viewsets as rmf_views
api_router = routers.SimpleRouter()


api_router.register(r'controls', rmf_views.NistControlViewSet)
api_router.register(r'ccis', rmf_views.ControlCorrelationIdentifierViewSet)
api_router.register(r'nist-statements', rmf_views.NistStatementViewSet)
