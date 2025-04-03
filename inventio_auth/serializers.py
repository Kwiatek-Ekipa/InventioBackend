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
