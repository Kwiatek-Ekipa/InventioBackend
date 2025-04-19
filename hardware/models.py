import uuid
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from inventio_auth.models import Account


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2)])


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=128)
    year_of_production = models.IntegerField(validators=[MinValueValidator(1950)])
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=128)