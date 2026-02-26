from rest_framework import viewsets

from ..models import BurgerQuiz
from ..serializers import BurgerQuizSerializer


class BurgerQuizViewSet(viewsets.ModelViewSet):
    """ViewSet pour le modèle BurgerQuiz."""

    queryset = BurgerQuiz.objects.all().order_by("-created_at")
    serializer_class = BurgerQuizSerializer
