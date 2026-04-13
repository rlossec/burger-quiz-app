from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import Nuggets
from ..serializers import NuggetsSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les manches Nuggets",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer une manche Nuggets",
        description="Auteur assigné automatiquement si JWT valide.",
        request=NuggetsSerializer,
        responses={201: NuggetsSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une manche Nuggets",
        responses={200: NuggetsSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une manche Nuggets",
        request=NuggetsSerializer,
        responses={200: NuggetsSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une manche Nuggets",
        request=NuggetsSerializer,
        responses={200: NuggetsSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une manche Nuggets",
        responses={204: None},
    ),
)
@extend_schema(tags=["Manche Nuggets"])
class NuggetsViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Nuggets (manche Nuggets)."""

    queryset = Nuggets.objects.all().order_by("title")
    serializer_class = NuggetsSerializer
