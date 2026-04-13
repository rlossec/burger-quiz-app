from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import VideoInterlude
from ..serializers import VideoInterludeSerializer, VideoInterludeListSerializer
from .base import AuthorAutoAssignMixin


@extend_schema_view(
    list=extend_schema(
        summary="Lister les interludes vidéo",
        description=(
            "Liste paginée. Filtres query : `tag` (nom insensible à la casse), "
            "`search` (recherche dans le titre)."
        ),
        parameters=[
            OpenApiParameter(
                name="tag",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
    ),
    create=extend_schema(
        summary="Créer une interlude vidéo",
        description="Crée une interlude ; auteur assigné automatiquement si JWT valide.",
        request=VideoInterludeSerializer,
        responses={201: VideoInterludeSerializer},
    ),
    retrieve=extend_schema(
        summary="Lire une interlude vidéo",
        responses={200: VideoInterludeSerializer},
    ),
    update=extend_schema(
        summary="Remplacer une interlude vidéo",
        request=VideoInterludeSerializer,
        responses={200: VideoInterludeSerializer},
    ),
    partial_update=extend_schema(
        summary="Mettre à jour partiellement une interlude vidéo",
        request=VideoInterludeSerializer,
        responses={200: VideoInterludeSerializer},
    ),
    destroy=extend_schema(
        summary="Supprimer une interlude vidéo",
        description=(
            "Refus (400) si l'interlude est référencée dans la structure d'un Burger Quiz."
        ),
        responses={204: None},
    ),
)
@extend_schema(tags=["Interludes vidéo"])
class VideoInterludeViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour les interludes vidéo."""

    def get_queryset(self):
        queryset = VideoInterlude.objects.all().order_by("-created_at")

        tag = self.request.query_params.get("tag")
        if tag:
            queryset = queryset.filter(tags__name__iexact=tag).distinct()

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return VideoInterludeListSerializer
        return VideoInterludeSerializer

    def destroy(self, request, *args, **kwargs):
        """Empêche la suppression si l'interlude est utilisé."""
        instance = self.get_object()
        if instance.structure_usages.exists():
            return Response(
                {"detail": "Cet interlude est utilisé dans un ou plusieurs Burger Quiz."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
