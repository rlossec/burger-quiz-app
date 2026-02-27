from rest_framework import viewsets

from ..models import DeadlyBurger
from ..serializers import DeadlyBurgerSerializer
from .base import AuthorAutoAssignMixin


class DeadlyBurgerViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle DeadlyBurger (manche Burger de la mort)."""

    queryset = DeadlyBurger.objects.all().order_by("title")
    serializer_class = DeadlyBurgerSerializer
