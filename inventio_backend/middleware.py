from django.http import QueryDict
from django.utils.deprecation import MiddlewareMixin
from djangorestframework_camel_case.util import camel_to_underscore

class CamelCaseQueryParamsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != 'GET':
            return

        parsed_params = {}
        for key, value in request.GET.items():
            param_parsed_key = camel_to_underscore(key)
            param_value_list = request.GET.getlist(key)

            if len(param_value_list) == 1:
                parsed_params.update({param_parsed_key: value})
            else:
                parsed_params.update({param_parsed_key: ','.join(param_value_list)})

        query_string = '&'.join([f"{key}={value}" for key, value in parsed_params.items()])
        request.GET = QueryDict(query_string, False)