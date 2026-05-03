from django.db import transaction

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ..models import BurgerQuizElement, Round
from .structure import (
    STRUCTURE_TYPE_TO_MODEL,
    parse_structure_element,
    structure_elements_to_representation,
)


class BurgerQuizStructureSerializer(serializers.Serializer):
    """PUT /structure/ — implicit order = position in the elements array."""

    elements = serializers.ListField(child=serializers.DictField(), allow_empty=True)

    def validate(self, attrs):
        raw_list = self.initial_data.get("elements")
        if raw_list is None:
            raise serializers.ValidationError({"elements": "Ce champ est requis."})
        if not isinstance(raw_list, list):
            raise serializers.ValidationError({"elements": "Une liste est attendue."})

        resolved: list[tuple[str, object]] = []
        seen_round_slugs: set[str] = set()
        seen_round_ids: set = set()

        for raw in raw_list:
            if not isinstance(raw, dict):
                raise serializers.ValidationError({"elements": "Chaque élément doit être un objet."})
            slug, oid = parse_structure_element(raw)

            model = STRUCTURE_TYPE_TO_MODEL.get(slug)
            if not model:
                raise serializers.ValidationError({"elements": f"Type inconnu : {slug!r}."})

            obj = model.objects.filter(pk=oid).first()
            if obj is None:
                raise serializers.ValidationError(
                    {"elements": f"Aucun objet {slug} pour l'id {oid}."}
                )

            if slug == "video_interlude":
                resolved.append((slug, oid))
                continue

            if slug in seen_round_slugs:
                raise serializers.ValidationError(
                    {
                        "elements": "Chaque type de manche (nuggets, sel ou poivre, …) ne peut apparaître qu'une fois."
                    }
                )
            seen_round_slugs.add(slug)

            if oid in seen_round_ids:
                raise serializers.ValidationError(
                    {"elements": "Une même manche ne peut apparaître qu'une seule fois."}
                )
            seen_round_ids.add(oid)

            resolved.append((slug, oid))

        attrs["resolved_elements"] = resolved
        return attrs

    @transaction.atomic
    def update(self, burger_quiz, validated_data):
        resolved = validated_data.get("resolved_elements", [])

        BurgerQuizElement.objects.filter(burger_quiz=burger_quiz).delete()

        for order, (slug, oid) in enumerate(resolved, start=1):
            if slug == "video_interlude":
                BurgerQuizElement.objects.create(
                    burger_quiz=burger_quiz,
                    order=order,
                    element_type=BurgerQuizElement.ElementType.INTERLUDE,
                    interlude_id=oid,
                    round=None,
                )
            else:
                round_obj = Round.objects.get(pk=oid)
                BurgerQuizElement.objects.create(
                    burger_quiz=burger_quiz,
                    order=order,
                    element_type=BurgerQuizElement.ElementType.ROUND,
                    round=round_obj,
                    interlude=None,
                )

        return burger_quiz


class BurgerQuizStructureReadSerializer(serializers.Serializer):
    """GET /structure/ — detailed view of the rounds (editor)."""

    burger_quiz_id = serializers.UUIDField(source="id")
    elements = serializers.SerializerMethodField()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_elements(self, burger_quiz):
        return structure_elements_to_representation(burger_quiz, expand_full=True)
