from django.contrib.auth import get_user_model
from rest_framework import serializers

from hardware.models import Category
from hardware.models import Brand
from hardware.models import Device

class HardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class AddedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "name", "surname"]

class DeviceSerializer(serializers.ModelSerializer):
    brand_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True)
    brand = BrandSerializer(read_only=True)
    category = HardwareCategorySerializer(read_only=True)
    added_by = AddedBySerializer(read_only=True)

    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {
            'added_by': {'read_only': True},
        }