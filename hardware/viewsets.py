from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from hardware.filters import HardwareCategoryOrderingFilter
from hardware.models import Category
from hardware.serializers import CreateHardwareCategorySerializer, HardwareCategorySerializer
from inventio_auth import IsTechnician


class HardwareCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = [HardwareCategoryOrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsTechnician]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in  ['retrieve', 'list']:
            return HardwareCategorySerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CreateHardwareCategorySerializer
        else:
            return HardwareCategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        name_query = self.request.query_params.get('name', None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        return queryset


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='name',
                description='Filter categories by name (case-insensitive substring match)',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='sort',
                description='Sort by name. Use `ascending` for ascending or `descending` for descending.',
                required=False,
                type=str,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)