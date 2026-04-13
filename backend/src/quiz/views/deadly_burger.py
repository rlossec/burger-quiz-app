from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from ..models import DeadlyBurger
from ..serializers import DeadlyBurgerSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les manches Burger de la mort",
        description="Liste paginée, tri par titre.",
    ),
    create=extend_schema(
        summary="Créer une manche Burger de la mort",
        description="Auteur assigné automatiquement si JWT valide.",
        request=DeadlyBurgerSerializer,
        responses={201: DeadlyBurgerSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une manche Burger de la mort",
        responses={200: DeadlyBurgerSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une manche Burger de la mort",
        request=DeadlyBurgerSerializer,
        responses={200: DeadlyBurgerSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une manche Burger de la mort",
        request=DeadlyBurgerSerializer,
        responses={200: DeadlyBurgerSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une manche Burger de la mort",
        responses={204: None},
    ),
)
@extend_schema(tags=["Manche Burger de la mort"])
class DeadlyBurgerViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle DeadlyBurger (manche Burger de la mort)."""

    queryset = DeadlyBurger.objects.all().order_by("title")
    serializer_class = DeadlyBurgerSerializer
