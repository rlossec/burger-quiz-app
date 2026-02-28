from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from ..models import BurgerQuizElement, VideoInterlude, ElementType, QuestionType
from .video_interlude import VideoInterludeMinimalSerializer


class BurgerQuizElementReadSerializer(serializers.ModelSerializer):
    """Serializer pour la lecture des éléments de structure."""

    interlude = VideoInterludeMinimalSerializer(read_only=True)

    class Meta:
        model = BurgerQuizElement
        fields = [
            "order",
            "element_type",
            "round_type",
            "interlude",
        ]
        read_only_fields = fields


class BurgerQuizElementWriteSerializer(serializers.Serializer):
    """Serializer pour l'écriture d'un élément de structure."""

    element_type = serializers.ChoiceField(choices=ElementType.choices)
    round_type = serializers.ChoiceField(
        choices=QuestionType.choices,
        required=False,
        allow_null=True,
    )
    interlude_id = serializers.UUIDField(required=False, allow_null=True)

    def validate(self, attrs):
        element_type = attrs.get("element_type")
        round_type = attrs.get("round_type")
        interlude_id = attrs.get("interlude_id")

        if element_type == ElementType.ROUND:
            if not round_type:
                raise serializers.ValidationError(
                    {"round_type": "Le type de manche est requis pour un élément de type 'round'."}
                )
            if interlude_id:
                raise serializers.ValidationError(
                    {"interlude_id": "Un élément de type 'round' ne peut pas avoir d'interlude."}
                )
        elif element_type == ElementType.INTERLUDE:
            if not interlude_id:
                raise serializers.ValidationError(
                    {"interlude_id": "L'ID de l'interlude est requis pour un élément de type 'interlude'."}
                )
            if round_type:
                raise serializers.ValidationError(
                    {"round_type": "Un élément de type 'interlude' ne peut pas avoir de type de manche."}
                )
            if not VideoInterlude.objects.filter(id=interlude_id).exists():
                raise serializers.ValidationError(
                    {"interlude_id": "L'interlude référencé n'existe pas."}
                )

        return attrs


class BurgerQuizStructureSerializer(serializers.Serializer):
    """Serializer pour la structure complète d'un Burger Quiz."""

    burger_quiz_id = serializers.UUIDField(read_only=True)
    elements = BurgerQuizElementWriteSerializer(many=True)

    def validate_elements(self, elements):
        """Valide les éléments de la structure."""
        round_types_seen = set()

        for element in elements:
            if element.get("element_type") == ElementType.ROUND:
                round_type = element.get("round_type")
                if round_type in round_types_seen:
                    raise serializers.ValidationError(
                        f"Chaque type de manche ne peut apparaître qu'une seule fois. "
                        f"'{round_type}' est dupliqué."
                    )
                round_types_seen.add(round_type)

        return elements

    def validate(self, attrs):
        """Valide que les manches référencées sont attachées au Burger Quiz."""
        burger_quiz = self.context.get("burger_quiz")
        if not burger_quiz:
            return attrs

        elements = attrs.get("elements", [])
        round_type_to_field = {
            QuestionType.NU: "nuggets",
            QuestionType.SP: "salt_or_pepper",
            QuestionType.ME: "menus",
            QuestionType.AD: "addition",
            QuestionType.DB: "deadly_burger",
        }

        for element in elements:
            if element.get("element_type") == ElementType.ROUND:
                round_type = element.get("round_type")
                field_name = round_type_to_field.get(round_type)
                if field_name and getattr(burger_quiz, field_name) is None:
                    raise serializers.ValidationError(
                        {
                            "elements": f"La manche '{round_type}' n'est pas attachée au Burger Quiz."
                        }
                    )

        return attrs

    def create(self, validated_data):
        """Non utilisé - voir update."""
        raise NotImplementedError("Utilisez update() pour modifier la structure.")

    def update(self, burger_quiz, validated_data):
        """Remplace la structure du Burger Quiz."""
        elements_data = validated_data.get("elements", [])

        BurgerQuizElement.objects.filter(burger_quiz=burger_quiz).delete()

        elements_to_create = []
        for order, element_data in enumerate(elements_data, start=1):
            element_type = element_data["element_type"]
            round_type = element_data.get("round_type")
            interlude_id = element_data.get("interlude_id")

            element = BurgerQuizElement(
                burger_quiz=burger_quiz,
                order=order,
                element_type=element_type,
                round_type=round_type if element_type == ElementType.ROUND else None,
                interlude_id=interlude_id if element_type == ElementType.INTERLUDE else None,
            )
            elements_to_create.append(element)

        BurgerQuizElement.objects.bulk_create(elements_to_create)

        return burger_quiz


class BurgerQuizStructureReadSerializer(serializers.Serializer):
    """Serializer pour la lecture de la structure."""

    burger_quiz_id = serializers.UUIDField(source="id")
    elements = serializers.SerializerMethodField()

    @extend_schema_field(BurgerQuizElementReadSerializer(many=True))
    def get_elements(self, burger_quiz):
        elements = burger_quiz.structure_elements.all().order_by("order")
        return BurgerQuizElementReadSerializer(elements, many=True).data
