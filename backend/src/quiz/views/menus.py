from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import Menus
from ..serializers import MenusSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les manches Menus",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer une manche Menus",
        description="Regroupe trois thèmes de menu. Auteur assigné automatiquement si JWT valide.",
        request=MenusSerializer,
        responses={201: MenusSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une manche Menus",
        responses={200: MenusSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une manche Menus",
        request=MenusSerializer,
        responses={200: MenusSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une manche Menus",
        request=MenusSerializer,
        responses={200: MenusSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une manche Menus",
        responses={204: None},
    ),
)
@extend_schema(tags=["Manche Menus"])
class MenusViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Menus (manche Menus, regroupe 3 thèmes)."""

    queryset = Menus.objects.all().order_by("title")
    serializer_class = MenusSerializer
