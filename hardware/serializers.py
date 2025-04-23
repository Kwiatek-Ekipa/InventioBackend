from rest_framework import serializers

from hardware.models import Category


class CreateHardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, data):
        category_name = data['name']
        category_name_no_whitespaces = "".join(category_name.split())
        if category_name_no_whitespaces == "":
            raise serializers.ValidationError({"name": "Name cannot be empty or contain only whitespaces"})
        if not category_name_no_whitespaces.isalpha():
            raise serializers.ValidationError({"name": "Name must contain only letters and whitespaces"})
        if len(category_name_no_whitespaces) < 2:
            raise serializers.ValidationError({"name": "Name must be greater or equal to 2 characters"})
        if len(category_name_no_whitespaces) > 128:
            raise serializers.ValidationError({"name": "Name must be less than 128 characters"})

        if Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError({"name": "A category with this name already exists."})
        return data

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

class HardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"