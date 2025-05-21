from itertools import chain

class FilterMultipleMixin:
    def filter_multiple(self, queryset, name, _value):
        raw_values = self.request.GET.getlist(name)
        param_list = [raw_value.split(',') for raw_value in raw_values]
        flat_param_list = list(chain.from_iterable(param_list))
        print(flat_param_list)

        return queryset.filter(**{f"{name}__in": flat_param_list})