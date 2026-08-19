from rest_framework.pagination import CursorPagination

class UserCursorPagination(CursorPagination):
    page_size=10
    ordering="id"
    page_size_quey_param="page_size"
    max_page_size=50