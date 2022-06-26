from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class QuestionPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 15

    def get_paginated_response(self, data):
        # response = Response(data)
        # response['count'] = self.page.paginator.count
        # response['total_pages'] = self.page.paginator.num_pages
        # response['next'] = self.get_next_link()
        # response['previous'] = self.get_previous_link()
        # return response
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'questions': data
        })
