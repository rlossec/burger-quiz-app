from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..models import DeadlyBurger
from ..serializers import DeadlyBurgerSerializer
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Manche Burger de la mort"])
class DeadlyBurgerViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle DeadlyBurger (manche Burger de la mort)."""

    queryset = DeadlyBurger.objects.all().order_by("title")
    serializer_class = DeadlyBurgerSerializer
