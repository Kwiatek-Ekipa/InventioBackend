from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from hardware.serializers import CreateHardwareCategorySerializer
from inventio_auth import is_technician



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@is_technician
def create_category(request):
    serializer = CreateHardwareCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)