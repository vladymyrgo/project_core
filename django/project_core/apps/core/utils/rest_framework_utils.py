from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    max_limit = settings.REST_FRAMEWORK['MAX_LIMIT']
