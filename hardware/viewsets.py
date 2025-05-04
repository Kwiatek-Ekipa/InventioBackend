from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, OpenApiParameter

from hardware.models import Device
from hardware.serializers import HardwareCategorySerializer, DeviceSerializer
from hardware.serializers import BrandSerializer
from inventio_auth import IsTechnician


class HardwareCategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = HardwareCategorySerializer
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
            OpenApiParameter(
                name = 'name',
                description = 'Filter results by category name (case-insensitive, partial match supported)',
                required = False,
                type = str,
                location = OpenApiParameter.QUERY
            )
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsTechnician]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'name',
                description = 'Filter results by brand name (case-insensitive, partial match supported)',
                required = False,
                type = str,
                location = OpenApiParameter.QUERY
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        name_query = self.request.query_params.get('name', '')
        if name_query:
            return BrandSerializer.Meta.model.objects.filter(name__icontains=name_query)
        return BrandSerializer.Meta.model.objects.all()


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'brand_id': ['exact'],
        'category_id': ['exact'],
        'model': ['icontains'],
        'serial_number': ['icontains'],
        'year_of_production': ['gte', 'lte'],
    }
    ordering_fields = ['year_of_production', 'model', 'serial_number', 'added_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsTechnician()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role.name == 'WORKER':
            return Device.objects.filter(added_by=user)
        return Device.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='brand_id', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='category_id', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='model', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='serial_number', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='year_of_production__gte', type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='year_of_production__lte', type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='ordering', type=str, location=OpenApiParameter.QUERY),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)