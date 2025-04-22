import uuid

from drf_yasg import openapi
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .enums import RoleEnum
from .permissions import IsTechnician
from .serializers import UserRegisterSerializer, UserInfoSerializer, CreateTechnicianSerializer
from .models import Account


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request: Request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: UserInfoSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request: Request):
    user = request.user
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=CreateTechnicianSerializer)
@api_view(['POST'])
@permission_classes([IsTechnician])
def create_technician(request: Request):
    serializer = CreateTechnicianSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete',
                     manual_parameters=[openapi.Parameter('user_id', openapi.IN_PATH, type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID)])
@api_view(['DELETE'])
@permission_classes([IsTechnician])
def delete_technician(request: Request, user_id: uuid.UUID):
    try:
        user_to_delete = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user == user_to_delete:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if user_to_delete.role.name != RoleEnum.TECHNICIAN.value:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    technician_count = Account.objects.filter(role__name=RoleEnum.TECHNICIAN.value).count()
    if technician_count <= 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
