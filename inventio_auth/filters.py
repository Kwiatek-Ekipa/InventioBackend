import django_filters
from django.contrib.auth import get_user_model


class AccountFilter(django_filters.FilterSet):
    role_id = django_filters.BaseInFilter(field_name='role_id', lookup_expr='in')

    class Meta:
        model = get_user_model()
        fields = ['role_id']