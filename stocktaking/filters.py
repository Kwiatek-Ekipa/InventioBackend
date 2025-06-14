import django_filters

from stocktaking.models import Stocktaking

class StocktakingFilter(django_filters.FilterSet):
    released_by_name = django_filters.CharFilter(
        field_name='released_by__name',
        lookup_expr='icontains'
    )
    released_by_surname = django_filters.CharFilter(
        field_name='released_by__surname',
        lookup_expr='icontains'
    )
    taken_back_by_name = django_filters.CharFilter(
        field_name='taken_back_by__name',
        lookup_expr='icontains'
    )
    taken_back_by_surname = django_filters.CharFilter(
        field_name='taken_back_by__surname',
        lookup_expr='icontains'
    )
    released_for_name = django_filters.CharFilter(
        field_name='recipient__name',
        lookup_expr='icontains'
    )
    released_for_surname = django_filters.CharFilter(
        field_name='recipient__surname',
        lookup_expr='icontains'
    )
    device_model = django_filters.CharFilter(
        field_name='device__model',
        lookup_expr='icontains'
    )
    device_serial_number = django_filters.CharFilter(
        field_name='device__serial_number',
        lookup_expr='icontains'
    )

    is_returned = django_filters.BooleanFilter(method='filter_missing_return_info')

    def filter_missing_return_info(self, queryset, name, value):
        if type(value) == bool:
            return queryset.filter(taken_back_by__isnull= not value, return_date__isnull= not value)
        return queryset


    class Meta:
        model = Stocktaking
        fields = []
