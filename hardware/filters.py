import django_filters
from hardware.models import Device


class DeviceFilter(django_filters.FilterSet):
    brand_id = django_filters.BaseInFilter(field_name='brand_id', lookup_expr='in')
    category_id = django_filters.BaseInFilter(field_name='category_id', lookup_expr='in')
    model = django_filters.CharFilter(field_name='model', lookup_expr='icontains')
    serial_number = django_filters.CharFilter(field_name='serial_number', lookup_expr='icontains')
    year_of_production__gte = django_filters.NumberFilter(field_name='year_of_production', lookup_expr='gte')
    year_of_production__lte = django_filters.NumberFilter(field_name='year_of_production', lookup_expr='lte')

    class Meta:
        model = Device
        fields = []
