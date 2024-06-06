from rest_framework.pagination import PageNumberPagination,CursorPagination,LimitOffsetPagination

class PostNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "record"
    max_page_size = 3
    last_page_strings = "last"
    
class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 4
    limit_query_param = "records"
    offset_query_param = "start"
    
class PostCursorPagination(CursorPagination):
    page_size = 3
    ordering = "posted_at"