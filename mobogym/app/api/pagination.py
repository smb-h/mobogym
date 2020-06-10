from rest_framework import pagination
from rest_framework.response import Response


# Post Pagination
class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    # overRide page_size
    # http://localhost:8000/en/Blog/API/?size=6
    page_size_query_param = 'size'
    max_page_size = 90

    # overRide Default Response
    def get_paginated_response(self, data):

        context = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
        }

        return Response(context)
