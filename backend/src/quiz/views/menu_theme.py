from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import MenuTheme
from ..serializers import MenuThemeSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les thèmes de menu",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer un thème de menu",
        description="Auteur assigné automatiquement si JWT valide.",
        request=MenuThemeSerializer,
        responses={201: MenuThemeSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire un thème de menu",
        responses={200: MenuThemeSerializer},
    ),
    update=extend_schema(
        summary="Remplacer un thème de menu",
        request=MenuThemeSerializer,
        responses={200: MenuThemeSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement un thème de menu",
        request=MenuThemeSerializer,
        responses={200: MenuThemeSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer un thème de menu",
        responses={204: None},
    ),
)
@extend_schema(tags=["Thèmes de menu"])
class MenuThemeViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle MenuTheme (thème de menu)."""

    queryset = MenuTheme.objects.all().order_by("title")
    serializer_class = MenuThemeSerializer
