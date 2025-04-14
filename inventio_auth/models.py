from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import uuid
from django.core.validators import MinLengthValidator

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])



class CustomUser(AbstractBaseUser):
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
