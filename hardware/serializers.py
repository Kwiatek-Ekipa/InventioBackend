from rest_framework import serializers

from hardware.models import Category
from hardware.models import Brand

class HardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"