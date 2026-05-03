from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer

from ..models import Addition, Question
from ..models.enums import QuestionType
from ..models.addition import AdditionQuestion
from .base import AuthorSerializer
from .question import QuestionSerializer


class AdditionSerializer(TaggitSerializer, ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Addition
        fields = ["id", "title", "description", "original", "author", "tags", "created_at", "updated_at", "questions", "question_ids"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
            "original": {"required": False},
        }

    @extend_schema_field(QuestionSerializer(many=True))
    def get_questions(self, obj):
        """Retourne les questions avec leur contenu complet (texte, réponses)."""
        ordered_qs = AdditionQuestion.objects.filter(addition=obj).order_by("order")
        questions = [aq.question for aq in ordered_qs]
        return QuestionSerializer(questions, many=True).data

    def to_internal_value(self, data):
        """Accepte 'questions' comme alias de 'question_ids' en entrée."""
        if "questions" in data and "question_ids" not in data:
            data = data.copy()
            data["question_ids"] = data.pop("questions")
        return super().to_internal_value(data)

    def validate(self, attrs):
        questions = attrs.get("question_ids")
        if questions is not None:
            # Pas de doublons
            if len(questions) != len(set(questions)):
                raise serializers.ValidationError({"question_ids": "Les IDs de questions ne doivent pas être dupliqués."})

            # Vérifier que toutes les questions existent
            existing_questions = Question.objects.filter(id__in=questions)
            if existing_questions.count() != len(questions):
                raise serializers.ValidationError({"question_ids": "Les IDs de questions ne doivent pas être inexistants."})

            # Vérifier que toutes les questions sont de type AD
            non_ad_questions = existing_questions.exclude(question_type=QuestionType.AD)
            if non_ad_questions.exists():
                raise serializers.ValidationError({"question_ids": "Toutes les questions doivent être de type Addition (AD)."})

        return attrs

    def create(self, validated_data):
        question_ids = validated_data.pop("question_ids", [])
        with transaction.atomic():
            addition = Addition.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                AdditionQuestion.objects.create(addition=addition, question_id=qid, order=order)
        return addition

    def update(self, instance, validated_data):
        question_ids = validated_data.pop("question_ids", None)
        tags = validated_data.pop("tags", None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    AdditionQuestion.objects.create(addition=instance, question_id=qid, order=order)

            if tags is not None:
                instance.tags.set(tags)

        return instance
