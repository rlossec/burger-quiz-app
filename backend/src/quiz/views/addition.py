from rest_framework import viewsets

from ..models import Addition
from ..serializers import AdditionSerializer
from .base import AuthorAutoAssignMixin


class AdditionViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Addition (manche Addition)."""

    queryset = Addition.objects.all().order_by("title")
    serializer_class = AdditionSerializer
