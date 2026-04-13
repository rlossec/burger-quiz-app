from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import SaltOrPepper
from ..serializers import SaltOrPepperSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les manches Sel ou poivre",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer une manche Sel ou poivre",
        description="Auteur assigné automatiquement si JWT valide.",
        request=SaltOrPepperSerializer,
        responses={201: SaltOrPepperSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une manche Sel ou poivre",
        responses={200: SaltOrPepperSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une manche Sel ou poivre",
        request=SaltOrPepperSerializer,
        responses={200: SaltOrPepperSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une manche Sel ou poivre",
        request=SaltOrPepperSerializer,
        responses={200: SaltOrPepperSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une manche Sel ou poivre",
        responses={204: None},
    ),
)
@extend_schema(tags=["Manche Sel ou poivre"])
class SaltOrPepperViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle SaltOrPepper (manche Sel ou poivre)."""

    queryset = SaltOrPepper.objects.all().order_by("title")
    serializer_class = SaltOrPepperSerializer
