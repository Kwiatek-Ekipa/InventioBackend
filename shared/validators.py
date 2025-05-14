from datetime import datetime

from rest_framework.exceptions import ValidationError


def no_only_digits(value: str):
    if value.isdigit():
        raise ValidationError('The value cannot be made up of digits only. Please include at least one letter.')

def not_greater_than_current_year(value: int):
    now = datetime.now()
    if value > now.year:
        raise ValidationError('The value cannot be greater than the current year.')