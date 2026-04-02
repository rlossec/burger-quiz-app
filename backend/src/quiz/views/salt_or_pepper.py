from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from ..models import SaltOrPepper
from ..serializers import SaltOrPepperSerializer
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Manche Sel ou poivre"])
class SaltOrPepperViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle SaltOrPepper (manche Sel ou poivre)."""

    queryset = SaltOrPepper.objects.all().order_by("title")
    serializer_class = SaltOrPepperSerializer
