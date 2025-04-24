from rest_framework.exceptions import ValidationError


def no_only_digits(value: str):
    if value.isdigit():
        raise ValidationError('Only digits are not allowed.')