from rest_framework.filters import OrderingFilter


class HardwareCategoryOrderingFilter(OrderingFilter):
    ordering_param = 'sort'

    def get_ordering(self, request, queryset, view):
        param = request.query_params.get(self.ordering_param)

        if param == 'ascending':
            return ['name']
        elif param == 'descending':
            return ['-name']
        return self.get_default_ordering(view)
