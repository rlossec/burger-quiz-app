from rest_framework.pagination import PageNumberPagination

from djoser import views


class UserListPagination(PageNumberPagination):
    """Pagination limitée à la liste des utilisateurs."""

    page_size = 10


class UserViewSet(views.UserViewSet):
    """ViewSet utilisateur Djoser avec pagination opt-in sur l'action list."""

    pagination_class = UserListPagination
