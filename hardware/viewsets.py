import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, OpenApiParameter

from hardware.filters import DeviceFilter
from hardware.models import Device
from hardware.serializers import HardwareCategorySerializer, DeviceSerializer
from hardware.serializers import BrandSerializer
from shared import IsTechnician, RoleEnum


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
    filterset_class = DeviceFilter
    ordering_fields = ['year_of_production', 'model', 'added_date']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsTechnician()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Device.objects.none()

        user = self.request.user
        if user.role.name == RoleEnum.WORKER.value:
            return Device.objects.filter(stocktaking__user_id=user.id).distinct()
        return Device.objects.all()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='brand_id', type=uuid.UUID, location=OpenApiParameter.QUERY, many=True, explode=True),
            OpenApiParameter(name='category_id', type=uuid.UUID, location=OpenApiParameter.QUERY, many=True,
                             explode=True),
            OpenApiParameter(name='model', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='serial_number', type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='year_of_production__gte', type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(name='year_of_production__lte', type=int, location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name='ordering',
                type=str,
                location=OpenApiParameter.QUERY,
                description=(
                        "Sort results by one of the following fields: "
                        "`year_of_production`, `model`, `added_date`. "
                        "Prefix with `-` to sort descending (e.g., `-model`)."
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)