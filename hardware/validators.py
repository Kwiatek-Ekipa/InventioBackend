from rest_framework.exceptions import ValidationError


def no_only_digits(value: str):
    if value.isdigit():
        raise ValidationError('The value cannot be made up of digits only. Please include at least one letter.')