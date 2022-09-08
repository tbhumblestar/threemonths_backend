from rest_framework.pagination import LimitOffsetPagination

class OrderListPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit     = 50