from rest_framework import serializers

from hardware.models import Device
from hardware.serializers import UserSerializer, DeviceSerializer

from stocktaking.models import Stocktaking


class GeneralDeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'model']


class StocktakingSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    device = GeneralDeviceInfoSerializer(read_only=True)
    released_by = UserSerializer(read_only=True)
    taken_back_by = UserSerializer(read_only=True)

    class Meta:
        model = Stocktaking
        fields = [
            'id',
            'release_date',
            'return_date',
            'recipient',
            'device',
            'released_by',
            'taken_back_by'

        ]
        extra_kwargs = {
            'released_by' : { 'read_only': True },
            'release_date' : { 'read_only': True },
            'device' : { 'read_only': True }
        }

class DetailedStocktakingSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()
    device = DeviceSerializer()
    released_by = UserSerializer()
    taken_back_by = UserSerializer()

    class Meta:
        model = Stocktaking
        fields = [
            'id',
            'release_date',
            'return_date',
            'recipient',
            'device',
            'released_by',
            'taken_back_by'

        ]


class TakeBackStocktakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocktaking
        fields = ['id']