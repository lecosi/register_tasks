# Django
from django.core.paginator import InvalidPage

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TaskInfoPagination(PageNumberPagination):

    page_size = 10
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get('size'):
            self.page_size = request.query_params.get('size')
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            msg = f'{self.page_query_param} param: {page_number} invalid'
            raise NotFound({
                'component': 'task',
                'msg': msg
            })

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'tasks': data,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            }
        })
