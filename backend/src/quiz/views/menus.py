from rest_framework import viewsets

from ..models import Menus
from ..serializers import MenusSerializer


class MenusViewSet(viewsets.ModelViewSet):
    """ViewSet pour le modèle Menus (manche Menus, regroupe 3 thèmes)."""

    queryset = Menus.objects.all().order_by("title")
    serializer_class = MenusSerializer
