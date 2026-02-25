from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Nuggets, Question
from ..models.enums import QuestionType
from ..models.nugget import NuggetQuestion


class NuggetsSerializer(ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Nuggets
        fields = ["id", "title", "original", "questions", "question_ids"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    def get_questions(self, obj):
        return [str(q.id) for q in obj.questions.all()]

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
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    NuggetQuestion.objects.create(nuggets=instance, question_id=qid, order=order)
        return instance
