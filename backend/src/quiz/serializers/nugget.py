from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer

from ..models import Nuggets, Question
from ..models.enums import QuestionType
from ..models.nugget import NuggetQuestion
from .base import AuthorSerializer
from .question import QuestionSerializer


class NuggetsSerializer(TaggitSerializer, ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Nuggets
        fields = ["id", "title", "original", "author", "tags", "created_at", "updated_at", "questions", "question_ids"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    @extend_schema_field(QuestionSerializer(many=True))
    def get_questions(self, obj):
        """Retourne les questions avec leur contenu complet (texte, réponses)."""
        ordered_qs = NuggetQuestion.objects.filter(nuggets=obj).order_by("order")
        questions = [nq.question for nq in ordered_qs]
        return QuestionSerializer(questions, many=True).data

    def validate_question_ids(self, value):
        if value is None:
            return value

        # Pas de doublons
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Les question_ids ne doivent pas contenir de doublons.")

        # Nombre pair
        if len(value) % 2 != 0:
            raise serializers.ValidationError("Le nombre de questions doit être pair.")

        # Vérifier que toutes les questions existent et sont de type NU
        questions = Question.objects.filter(id__in=value)
        if questions.count() != len(value):
            raise serializers.ValidationError("Une ou plusieurs questions n'existent pas.")

        non_nu_questions = questions.exclude(question_type=QuestionType.NU)
        if non_nu_questions.exists():
            raise serializers.ValidationError("Toutes les questions doivent être de type Nuggets (NU).")

        return value

    def create(self, validated_data):
        question_ids = validated_data.pop("question_ids", [])
        with transaction.atomic():
            nuggets = Nuggets.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                NuggetQuestion.objects.create(nuggets=nuggets, question_id=qid, order=order)
        return nuggets

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
                    NuggetQuestion.objects.create(nuggets=instance, question_id=qid, order=order)

            if tags is not None:
                instance.tags.set(tags)

        return instance
