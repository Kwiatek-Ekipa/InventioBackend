from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import BadRequest
from django.core.validators import MinLengthValidator
from django.db import models
import uuid

from inventio_auth.enums import RoleEnum


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, choices=RoleEnum.choices(), default=RoleEnum.WORKER, unique=True)

class AccountManager(BaseUserManager):
    def create(self, email, password=None, role: RoleEnum = RoleEnum.WORKER, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        try:
            role = Role.objects.get(name=role.value)
        except Role.DoesNotExist:
            raise BadRequest('Role does not exist')

        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Account(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])
    surname = models.CharField(max_length=128, validators=[MinLengthValidator(2)])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name', 'surname', 'role']

    objects = AccountManager()
