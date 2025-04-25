from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins

from inventio_auth import IsTechnician
from inventio_auth.models import Role
from inventio_auth.serializers import AccountSerializer, RoleSerializer


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class AccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    http_method_names = ['get', 'patch']
    permission_classes = [IsTechnician]
    serializer_class = AccountSerializer

    def get_queryset(self):
        query_string = self.request.query_params.get('q', '')
        if query_string:
            return self.serializer_class.Meta.model.objects.filter(Q(email__icontains=query_string) | Q(name__icontains=query_string) | Q(surname__icontains=query_string))
        return self.serializer_class.Meta.model.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name = 'q',
                description = 'Filter results by email, name or surname (case-insensitive, partial match supported)',
                required = False,
                type = str,
                location = OpenApiParameter.QUERY
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

