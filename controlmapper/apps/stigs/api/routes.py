from rest_framework import routers
from apps.stigs.api.v1.viewsets import BenchmarkViewSet, RuleViewSet, GroupViewSet

api_router = routers.SimpleRouter()


api_router.register(r'stigs', BenchmarkViewSet)
# api_router.register(r'profiles', stig_views.ProfileViewSet)
# api_router.register(r'profile-selects', stig_views.ProfileSelectViewSet)
api_router.register(r'rules', RuleViewSet)
api_router.register(r'groups', GroupViewSet)
