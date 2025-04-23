from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from hardware.serializers import BrandSerializer
from inventio_auth import IsTechnician

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = serializer_class.Meta.model.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsTechnician]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter('name', type=str, location=OpenApiParameter.QUERY, description='Brand name')
        ]
    )
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(name__icontains=request.query_params.get('name', ''))
        return super().list(request, *args, **kwargs)