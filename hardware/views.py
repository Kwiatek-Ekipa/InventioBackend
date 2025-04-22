from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hardware.models import Category
from hardware.serializers import CreateHardwareCategorySerializer, GetHardwareCategorySerializer, \
    HardwareCategorySerializer
from inventio_auth import IsTechnician


class HardwareCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsTechnician]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GetHardwareCategorySerializer
        elif self.action == 'list':
            return HardwareCategorySerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CreateHardwareCategorySerializer
        else:
            return HardwareCategorySerializer