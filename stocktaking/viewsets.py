from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from shared import IsTechnician, RoleEnum
from stocktaking.models import Stocktaking
from stocktaking.serializers import StocktakingSerializer


class StocktakingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete']
    serializer_class = StocktakingSerializer
    queryset = Stocktaking.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            permission_classes = [IsTechnician]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        queryset = Stocktaking.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        user = self.request.user

        if user.role.name == RoleEnum.WORKER.value and obj.user_id != user.id:
            raise PermissionDenied("You do not have permission to access this object.")

        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset()

        if user.role.name == RoleEnum.WORKER.value:
            queryset = queryset.filter(user_id=user.id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


