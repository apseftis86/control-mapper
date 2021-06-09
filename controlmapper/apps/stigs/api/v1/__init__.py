from rest_framework import viewsets, permissions
import django_filters.rest_framework


class STIGViewSet(viewsets.ModelViewSet):
    serializer_class = None
    serializer_detail_class = None
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'list':
            return super(STIGViewSet, self).get_serializer_class()
        else:
            return self.serializer_detail_class or self.serializer_class
