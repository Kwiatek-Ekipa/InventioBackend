from django.core.validators import MinLengthValidator
from django.db import models
import uuid


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])
    surname = models.CharField(max_length=128, validators=[MinLengthValidator(2)])
    role = models.ForeignKey(Role, on_delete=models.CASCADE)