from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import VideoInterlude
from ..serializers import VideoInterludeSerializer, VideoInterludeListSerializer
from .base import AuthorAutoAssignMixin


class VideoInterludeViewSet(AuthorAutoAssignMixin, viewsets.ModelViewSet):
    """ViewSet pour les interludes vidéo."""

    def get_queryset(self):
        queryset = VideoInterlude.objects.all().order_by("-created_at")

        interlude_type = self.request.query_params.get("interlude_type")
        if interlude_type:
            queryset = queryset.filter(interlude_type=interlude_type)

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
        if instance.burger_quiz_elements.exists():
            return Response(
                {"detail": "Cet interlude est utilisé dans un ou plusieurs Burger Quiz."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
