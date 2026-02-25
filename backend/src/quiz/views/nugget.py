from rest_framework import viewsets

from ..models import Nuggets
from ..serializers import NuggetsSerializer


class NuggetsViewSet(viewsets.ModelViewSet):
    """ViewSet pour le modèle Nuggets (manche Nuggets)."""

    queryset = Nuggets.objects.all().order_by("title")
    serializer_class = NuggetsSerializer
