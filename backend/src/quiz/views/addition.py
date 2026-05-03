from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import Addition
from ..serializers import AdditionSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les manches Addition",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer une manche Addition",
        description="Auteur assigné automatiquement si JWT valide.",
        request=AdditionSerializer,
        responses={201: AdditionSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une manche Addition",
        responses={200: AdditionSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une manche Addition",
        request=AdditionSerializer,
        responses={200: AdditionSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une manche Addition",
        request=AdditionSerializer,
        responses={200: AdditionSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une manche Addition",
        responses={204: None},
    ),
)
@extend_schema(tags=["Manche Addition"])
class AdditionViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Addition (manche Addition)."""

    queryset = Addition.objects.all().order_by("title")
    serializer_class = AdditionSerializer
