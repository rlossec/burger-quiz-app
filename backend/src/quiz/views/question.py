from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets, filters

from ..models import Question
from ..serializers import QuestionSerializer, QuestionListSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les questions",
        description=(
            "Liste paginée. `search` interroge le champ texte. "
            "Filtres : `question_type`, `original` (`true` / `false`), `author` (id), "
            "`tags` (noms séparés par des virgules)."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="question_type",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="original",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="`true` ou `false`",
            ),
            OpenApiParameter(
                name="author",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Identifiant (pk) de l'utilisateur auteur",
            ),
            OpenApiParameter(
                name="tags",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Noms de tags, séparés par des virgules",
            ),
        ],
    ),
    create=extend_schema(
        summary="Créer une question",
        description="Crée une question ; auteur assigné automatiquement si JWT valide.",
        request=QuestionSerializer,
        responses={201: QuestionSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une question",
        description="Détail avec réponses associées.",
        responses={200: QuestionSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une question",
        request=QuestionSerializer,
        responses={200: QuestionSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une question",
        request=QuestionSerializer,
        responses={200: QuestionSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une question",
        responses={204: None},
    ),
)
@extend_schema(tags=["Questions"])
class QuestionViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle Question."""

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
