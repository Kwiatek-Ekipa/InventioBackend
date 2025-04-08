from rest_framework import serializers
from django.contrib.auth import get_user_model
from inventio_auth.models import Role

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
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        try:
            default_role = Role.objects.get(name='Worker')
        except Role.DoesNotExist:
            raise serializers.ValidationError('Role does not exist')
        user = User.objects.create(**validated_data, role=default_role)
        user.set_password(password)
        user.save()
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
                f"Puste pola: {', '.join(missing_fields)}")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Hasła nie są zgodne.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        technician_role = Role.objects.get(name='Technician')
        user = User.objects.create(**validated_data, role = technician_role)
        user.set_password(password)
        user.save()
        return user




