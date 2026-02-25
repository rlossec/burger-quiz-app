from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Question
from ..models.answer import Answer
from ..models.enums import QuestionType
from .answer import AnswerSerializer


class AnswerWriteSerializer(serializers.Serializer):
    """Serializer pour la création/mise à jour des réponses (sans id)."""

    text = serializers.CharField()
    is_correct = serializers.BooleanField(default=False)


class QuestionSerializer(ModelSerializer):
    answers = AnswerWriteSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "question_type",
            "original",
            "explanations",
            "video_url",
            "image_url",
            "created_at",
            "updated_at",
            "answers",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "text": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
            "question_type": {"error_messages": {"required": "Ce champ est obligatoire."}},
        }

    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Ce champ ne peut pas être vide.")
        return value

    def validate(self, attrs):
        qtype = attrs.get("question_type")
        answers = attrs.get("answers", [])

        if qtype == QuestionType.NU:
            self._validate_nuggets(answers)
        elif qtype == QuestionType.SP:
            self._validate_salt_or_pepper(answers)
        elif qtype == QuestionType.ME:
            self._validate_menu(answers)
        elif qtype == QuestionType.AD:
            self._validate_addition(answers)
        elif qtype == QuestionType.DB:
            self._validate_deadly_burger(answers)

        return attrs

    def _validate_nuggets(self, answers):
        """NU: exactement 4 réponses, exactement 1 correcte."""
        if len(answers) != 4:
            raise serializers.ValidationError(
                {"answers": "Une question Nuggets doit avoir exactement 4 réponses."}
            )
        correct_count = sum(1 for a in answers if a.get("is_correct"))
        if correct_count != 1:
            raise serializers.ValidationError(
                {"answers": "Une question Nuggets doit avoir exactement 1 réponse correcte."}
            )

    def _validate_salt_or_pepper(self, answers):
        """SP: au moins 1 réponse, toutes correctes (pas de pièges)."""
        if not answers:
            raise serializers.ValidationError(
                {"answers": "Une question Sel ou Poivre doit avoir au moins une réponse."}
            )
        if any(not a.get("is_correct") for a in answers):
            raise serializers.ValidationError(
                {"answers": "Les questions ouvertes n'acceptent pas de réponses incorrectes."}
            )

    def _validate_menu(self, answers):
        """ME: au moins 1 réponse, toutes correctes (pas de pièges)."""
        if not answers:
            raise serializers.ValidationError(
                {"answers": "Une question Menu doit avoir au moins une réponse."}
            )
        if any(not a.get("is_correct") for a in answers):
            raise serializers.ValidationError(
                {"answers": "Les questions ouvertes n'acceptent pas de réponses incorrectes."}
            )

    def _validate_addition(self, answers):
        """AD: au moins 1 réponse correcte, pas de pièges."""
        if not answers:
            raise serializers.ValidationError(
                {"answers": "Une question Addition doit avoir au moins une réponse."}
            )
        if any(not a.get("is_correct") for a in answers):
            raise serializers.ValidationError(
                {"answers": "Les questions ouvertes n'acceptent pas de réponses incorrectes."}
            )

    def _validate_deadly_burger(self, answers):
        """DB: aucune réponse."""
        if answers:
            raise serializers.ValidationError(
                {"answers": "Une question Burger de la Mort ne doit pas avoir de réponses."}
            )

    def create(self, validated_data):
        answers_data = validated_data.pop("answers", [])
        with transaction.atomic():
            question = Question.objects.create(**validated_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if answers_data is not None:
                instance.answers.all().delete()
                for answer_data in answers_data:
                    Answer.objects.create(question=instance, **answer_data)
        return instance

    def to_representation(self, instance):
        """En lecture, utilise AnswerSerializer pour inclure les ids."""
        ret = super().to_representation(instance)
        ret["answers"] = AnswerSerializer(instance.answers.all(), many=True).data
        return ret


class QuestionListSerializer(QuestionSerializer):
    """Liste : pas d'answers pour alléger le payload."""

    class Meta(QuestionSerializer.Meta):
        fields = [
            "id",
            "text",
            "question_type",
            "original",
            "explanations",
            "video_url",
            "image_url",
            "created_at",
            "updated_at",
        ]
