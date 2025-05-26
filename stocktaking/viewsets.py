from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from shared import IsTechnician, RoleEnum
from stocktaking.filters import StocktakingFilter
from stocktaking.models import Stocktaking
from stocktaking.serializers import StocktakingSerializer, TakeBackStocktakingSerializer, DetailedStocktakingSerializer


class StocktakingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete']
    serializer_class = StocktakingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = StocktakingFilter
    ordering_fields = [
        'release_date',
        'return_date',
        'released_by__name',
        'released_by__surname',
        'taken_back_by__name',
        'taken_back_by__surname',
        'device__model',
        'recipient__name',
        'recipient__surname'
    ]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Stocktaking.objects.none()

        user = self.request.user

        if user.role.name == RoleEnum.WORKER.value:
            return Stocktaking.objects.filter(recipient_id=user.id)

        return Stocktaking.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return DetailedStocktakingSerializer
        else:
            return StocktakingSerializer

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy', 'take_back_device']:
            permission_classes = [IsTechnician]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self):
        queryset = Stocktaking.objects.all()
        obj = get_object_or_404(queryset, pk=self.kwargs["pk"])
        user = self.request.user

        if user.role.name == RoleEnum.WORKER.value and obj.recipient_id != user.id:
            raise PermissionDenied("You do not have permission to access this object.")

        self.check_object_permissions(self.request, obj)
        return obj

    def partial_update(self, request, *args, **kwargs):
        disallowed_fields = ['taken_back_by', 'return_date']
        for field in disallowed_fields:
            if field in request.data:
                return Response(
                    {"detail": f"Field '{field}' cannot be modified directly."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='ordering',
                type=str,
                location=OpenApiParameter.QUERY,
                description=(
                        "Sort results by one of the following fields: "
                        "`release_date`, `return_date`, `released_by__name`,"
                        "`released_by__surname`, `taken_back_by__name`,"
                        "`taken_back_by__surname`, `device__model`, `recipient__name`, `recipient__surname`."
                        "Prefix with `-` to sort descending (e.g., `-release_date`).`"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



    @extend_schema(
        parameters=[],
        request=TakeBackStocktakingSerializer,
    )
    @action(detail=True, methods=['patch'], url_path='take-back')
    def take_back_device(self, request, pk=None):
        stocktaking = self.get_object()

        if stocktaking.return_date is not None or stocktaking.taken_back_by is not None:
            return Response(
                {"detail": "This device has already been returned!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        stocktaking.return_date = request.data.get('return_date', now())
        stocktaking.taken_back_by = request.user
        stocktaking.save()

        serializer = self.get_serializer(stocktaking)
        return Response(serializer.data)
