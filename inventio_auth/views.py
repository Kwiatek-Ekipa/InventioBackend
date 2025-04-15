from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .enums import RoleEnum
from .permissions import is_technician
from .serializers import UserRegisterSerializer, UserInfoSerializer, CreateTechnicianSerializer
from .models import Account


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_technician
def create_technician(request):
    if request.method == 'POST':
        serializer = CreateTechnicianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@is_technician
def delete_technician(request, user_id):
    try:
        user_to_delete = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user == user_to_delete:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if user_to_delete.role.name != RoleEnum.TECHNICIAN:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    technician_count = Account.objects.filter(role__name=RoleEnum.TECHNICIAN).count()
    if technician_count <= 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user_to_delete.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)





