from drf_spectacular.utils import extend_schema, extend_schema_view
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


@extend_schema_view(
    list=extend_schema(
        summary="Lister les Burger Quiz",
        description="Liste paginée des Burger Quiz, du plus récent au plus ancien.",
    ),
    create=extend_schema(
        summary="Créer un Burger Quiz",
        description="Crée un quiz ; auteur assigné automatiquement si JWT valide.",
        request=BurgerQuizSerializer,
        responses={201: BurgerQuizSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire un Burger Quiz",
        description="Retourne le Burger Quiz avec sa structure.",
        responses={200: BurgerQuizSerializer},
    ),
    update=extend_schema(
        summary="Remplacer un Burger Quiz",
        description="Mise à jour complète (PUT).",
        request=BurgerQuizSerializer,
        responses={200: BurgerQuizSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement un Burger Quiz",
        description="Mise à jour partielle (PATCH).",
        request=BurgerQuizSerializer,
        responses={200: BurgerQuizSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer un Burger Quiz",
        description="Suppression définitive du quiz.",
        responses={204: None},
    ),
)
@extend_schema(tags=["Burger Quiz"])
class BurgerQuizViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    queryset = BurgerQuiz.objects.all().order_by("-created_at")
    serializer_class = BurgerQuizSerializer

    @extend_schema(
        methods=["GET"],
        summary="Lire la structure du Burger Quiz",
        description=(
            "Retourne l'ordre des manches et interludes du Burger Quiz."
        ),
        responses={200: BurgerQuizStructureReadSerializer},
    )
    @extend_schema(
        methods=["PUT"],
        summary="Remplacer la structure du Burger Quiz",
        description=(
            "Permet de personnaliser l'ordre des manches et interludes du Burger Quiz."
        ),
        request=BurgerQuizStructureSerializer,
        responses={200: BurgerQuizStructureReadSerializer},
    )
    @action(detail=True, methods=["get", "put"], url_path="structure", url_name="structure")
    def structure(self, request, pk=None):
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
