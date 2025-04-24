from rest_framework import serializers

from hardware.models import Category

class HardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"