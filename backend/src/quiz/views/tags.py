"""
Liste des noms de tags (django-taggit) pour autocomplétion côté client.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag

from ..utils import parse_positive_int


@extend_schema(
    tags=["Tags"],
    summary="Rechercher des noms de tags",
    description=(
        "Retourne une liste de noms de tags existants (django-taggit), filtrés par sous-chaîne "
        "insensible à la casse sur le nom. Utile pour l’autocomplétion dans les formulaires."
    ),
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Sous-chaîne recherchée dans le nom du tag (correspondance partielle).",
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Nombre maximum de résultats (1 à 100, défaut 20).",
        ),
    ],
    responses={
        200: {
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Noms de tags, triés par nom.",
                },
            },
        },
    },
)
class TagListAPIView(APIView):
    """GET — catalogue de tags pour autocomplétion."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        limit = parse_positive_int(
            request.query_params.get("limit"),
            default=20,
            minimum=1,
            maximum=100,
        )

        qs = Tag.objects.all().order_by("name")
        if q:
            qs = qs.filter(name__icontains=q)
        names = list(qs.values_list("name", flat=True)[:limit])
        return Response({"results": names})
