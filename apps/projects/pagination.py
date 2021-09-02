# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from rest_framework.pagination import PageNumberPagination


class PaginationSta(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100
