from rest_framework import viewsets

from ..models import BurgerQuiz
from ..serializers import BurgerQuizSerializer
from .base import AuthorAutoAssignMixin


class BurgerQuizViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle BurgerQuiz."""

    queryset = BurgerQuiz.objects.all().order_by("-created_at")
    serializer_class = BurgerQuizSerializer
