from rest_framework import serializers

from hardware.models import Category


class CreateHardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, data):
        if not data['name'].isalpha():
            raise serializers.ValidationError({"name": "Name must contain only letters and whitespaces"})
        if len(data['name']) < 2:
            raise serializers.ValidationError({"name": "Name must be greater or equal to 2 characters"})
        if len(data['name']) > 128:
            raise serializers.ValidationError({"name": "Name must be less than 128 characters"})
        # Something else already checks all the 3 conditions above and raises other error messages. Keeping it for double safety

        if Category.objects.filter(name=data['name']).exists():
            raise serializers.ValidationError({"name": "A category with this name already exists."})
        return data

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
