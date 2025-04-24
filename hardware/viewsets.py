from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from hardware.serializers import BrandSerializer
from inventio_auth import IsTechnician

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsTechnician]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        name_query = self.request.query_params.get('name', '')
        if name_query:
            return self.serializer_class.Meta.model.objects.filter(name__icontains=name_query)
        return self.serializer_class.Meta.model.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter('name', type=str, location=OpenApiParameter.QUERY, description='Filter results by brand name (case-insensitive, partial match supported)')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)