from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..models import Addition
from ..serializers import AdditionSerializer
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Manche Addition"])
class AdditionViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Addition (manche Addition)."""

    queryset = Addition.objects.all().order_by("title")
    serializer_class = AdditionSerializer
