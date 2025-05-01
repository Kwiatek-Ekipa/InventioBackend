import uuid
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Q, F, Func, Value

from hardware.validators import no_only_digits
from inventio_auth.models import Account


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2), no_only_digits], unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_brand_name',
                fields=['name']
            ),
            models.CheckConstraint(
                name='brand_name_min_length_2',
                condition=Q(name__regex=r'^.{2,}$')
            ),
            models.CheckConstraint(
                name='brand_name_not_only_digits',
                condition=~Q(name__regex=r'^\d+$')
            )
        ]


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, validators=[MinLengthValidator(2), no_only_digits], unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_category_name',
                fields=['name']
            ),
            models.CheckConstraint(
                name='category_name_min_length_2',
                condition=Q(name__regex=r'^.{2,}$')
            ),
            models.CheckConstraint(
                name='category_name_not_only_digits',
                condition=~Q(name__regex=r'^\d+$')
            )
        ]


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=128)
    year_of_production = models.IntegerField(validators=[MinValueValidator(1950)])
    added_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=128, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_serial_number',
                fields=['serial_number']
            ),
            models.CheckConstraint(
                name='year_of_production_min_value',
                condition=Q(year_of_production__gte=1950)
            )
        ]