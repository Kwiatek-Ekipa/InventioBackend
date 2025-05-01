from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import BadRequest
from django.core.validators import MinLengthValidator
from django.db import models
import uuid

from django.db.models import Q

from hardware.validators import no_only_digits
from inventio_auth.enums import RoleEnum


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, choices=RoleEnum.choices(), default=RoleEnum.WORKER, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="role_name_worker_or_technician",
                condition=models.Q(name__in=[RoleEnum.WORKER.value, RoleEnum.TECHNICIAN.value])
            )
        ]


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
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2), no_only_digits])
    surname = models.CharField(max_length=128, validators=[MinLengthValidator(2), no_only_digits])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name', 'surname', 'role']

    objects = AccountManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='valid_email_format',
                condition=Q(email__regex=r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'),
            ),
            models.CheckConstraint(
                name='name_min_length_2_and_only_letters',
                condition=Q(name__regex=r'^[^\W\d_]{2,}$')
            ),
            models.CheckConstraint(
                name='surname_min_length_2_and_only_letters',
                # Either minimum 2 characters (including non-ASCII letters, for example: "śżć")
                # or minimum 3 characters with the 1 hyphen in the middle
                condition=Q(surname__regex=r'^[^\W\d_]{2,}$') | Q(surname__regex=r'^[^\W\d_]+-[^\W\d_]+$')
            )
        ]
