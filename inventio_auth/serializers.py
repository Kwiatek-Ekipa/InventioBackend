from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from shared.enums import RoleEnum
from inventio_auth.models import Role

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirmation', 'name', 'surname']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        data.pop('password_confirmation')

        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already taken."})
        if not data['name'].isalpha():
            raise serializers.ValidationError({"name": "Name must contain only letters."})
        if not data['surname'].isalpha():
            raise serializers.ValidationError({"surname": "Surname must contain only letters."})

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data, role=RoleEnum.WORKER)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'role']


class CreateTechnicianSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        required_fields = ['name', 'surname', 'email', 'password', 'password_confirmation']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise serializers.ValidationError(
                f"Empty fields: {', '.join(missing_fields)}")
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match")
        data.pop('password_confirmation')

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data, role=RoleEnum.TECHNICIAN)
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class AccountSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'surname', 'role', 'role_id']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
            'name': {'read_only': True},
            'surname': {'read_only': True},
        }

    def update(self, instance, validated_data):
        role_id = validated_data.get('role_id', instance.role)
        role = Role.objects.get(id=role_id)
        instance.role = role
        instance.save()
        return instance