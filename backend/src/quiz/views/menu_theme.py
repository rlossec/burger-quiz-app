from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..models import MenuTheme
from ..serializers import MenuThemeSerializer
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Thèmes de menu"])
class MenuThemeViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle MenuTheme (thème de menu)."""

    queryset = MenuTheme.objects.all().order_by("title")
    serializer_class = MenuThemeSerializer
