from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..models import Nuggets
from ..serializers import NuggetsSerializer
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Manche Nuggets"])
class NuggetsViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Nuggets (manche Nuggets)."""

    queryset = Nuggets.objects.all().order_by("title")
    serializer_class = NuggetsSerializer
