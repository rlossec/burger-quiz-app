from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import BurgerQuiz
from ..serializers import (
    BurgerQuizSerializer,
    BurgerQuizStructureSerializer,
    BurgerQuizStructureReadSerializer,
)
from .base import AuthorAutoAssignMixin


@extend_schema(tags=["Burger Quiz"])
class BurgerQuizViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour le modèle BurgerQuiz."""

    queryset = BurgerQuiz.objects.all().order_by("-created_at")
    serializer_class = BurgerQuizSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="expand",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Valeur `full` : inclut la structure détaillée (manches et interludes complets).",
                required=False,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=["get", "put"], url_path="structure", url_name="structure")
    def structure(self, request, pk=None):
        """
        GET: Lecture de la structure du Burger Quiz.
        PUT: Remplacement de la structure du Burger Quiz.
        """
        burger_quiz = self.get_object()

        if request.method == "GET":
            serializer = BurgerQuizStructureReadSerializer(burger_quiz)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = BurgerQuizStructureSerializer(
                data=request.data,
                context={"burger_quiz": burger_quiz, "request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(burger_quiz, serializer.validated_data)

            read_serializer = BurgerQuizStructureReadSerializer(burger_quiz)
            return Response(read_serializer.data, status=status.HTTP_200_OK)
