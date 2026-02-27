from rest_framework import viewsets, filters

from ..models import Question
from ..serializers import QuestionSerializer, QuestionListSerializer
from .base import AuthorAutoAssignMixin


class QuestionViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """
    ViewSet pour le modèle Question.
    Liste : GET /api/quiz/questions/ (filtres search, question_type, original, author, tags).
    Détail : GET /api/quiz/questions/{id}/ (avec answers).
    """

    queryset = Question.objects.all().order_by("-created_at")
    filter_backends = [filters.SearchFilter]
    search_fields = ["text"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action != "list":
            return qs
        query_params = self.request.query_params
        if query_params.get("question_type"):
            qs = qs.filter(question_type=query_params["question_type"])
        if query_params.get("original") in ("true", "false"):
            qs = qs.filter(original=query_params["original"].lower() == "true")
        if query_params.get("author"):
            qs = qs.filter(author_id=query_params["author"])
        if query_params.get("tags"):
            tags = query_params["tags"].split(",")
            qs = qs.filter(tags__name__in=tags).distinct()
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return QuestionListSerializer
        return QuestionSerializer
