from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class NormalPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30

    def get_paginated_response(self, data):
        return Response({
            'count': self.get_count(data),
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'result': data
        })
