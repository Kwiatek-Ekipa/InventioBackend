from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventio_auth.models import Role
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from inventio_auth.enums import RoleEnum

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})
        if not data['first_name'].isalpha():
            raise serializers.ValidationError({"first_name": "First name must contain only letters."})
        if not data['last_name'].isalpha():
            raise serializers.ValidationError({"last_name": "Last name must contain only letters."})
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data, role=RoleEnum.WORKER)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'role']


class CreateTechnicianSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        required_fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError(
                f"Empty fields: {', '.join(missing_fields)}")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        data.pop('confirm_password')

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data, role=RoleEnum.TECHNICIAN)
        return user
