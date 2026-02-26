from rest_framework import viewsets

from ..models import MenuTheme
from ..serializers import MenuThemeSerializer


class MenuThemeViewSet(viewsets.ModelViewSet):
    """ViewSet pour le modèle MenuTheme (thème de menu)."""

    queryset = MenuTheme.objects.all().order_by("title")
    serializer_class = MenuThemeSerializer
