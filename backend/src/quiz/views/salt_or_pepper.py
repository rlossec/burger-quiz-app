from rest_framework import viewsets

from ..models import SaltOrPepper
from ..serializers import SaltOrPepperSerializer


class SaltOrPepperViewSet(viewsets.ModelViewSet):
    """ViewSet pour le modèle SaltOrPepper (manche Sel ou poivre)."""

    queryset = SaltOrPepper.objects.all().order_by("title")
    serializer_class = SaltOrPepperSerializer
