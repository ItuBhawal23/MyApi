from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
        page_query_param = 'page-num' #default = page (default = 1) Custom page number query param (from client)
        page_size_query_param = 'page_size' # upto defined no. of items in a page (Defaults to None)
        max_page_size = 10 # applicable only if using page_size_query_param. max no. of items in a page (higher precedence over page_size_query_param)
        page_size = 1

        def get_paginated_response(self, data):
            return Response({
                'links':{
                    'next': self.get_next_link(),
                    'prev': self.get_previous_link()
                },
                'count': self.page.paginator.count,

                # it will take the value from query param ?page_size=,
                # else fallback to `page_size` defined in the class or `PAGE_SIZE` from settings
                'page_size': self.get_page_size(self.request),
                'results': data
            })