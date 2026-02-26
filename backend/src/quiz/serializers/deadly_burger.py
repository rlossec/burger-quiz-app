from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import DeadlyBurger, Question
from ..models.enums import QuestionType
from ..models.deadly_burger import DeadlyBurgerQuestion


class DeadlyBurgerSerializer(ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeadlyBurger
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

        # Exactement 10 questions
        if len(value) != 10:
            raise serializers.ValidationError("La manche Burger de la mort doit contenir exactement 10 questions.")

        # Vérifier que toutes les questions existent
        questions = Question.objects.filter(id__in=value)
        if questions.count() != len(value):
            raise serializers.ValidationError("Une ou plusieurs questions n'existent pas.")

        # Vérifier que toutes les questions sont de type DB
        non_db_questions = questions.exclude(question_type=QuestionType.DB)
        if non_db_questions.exists():
            raise serializers.ValidationError("Toutes les questions doivent être de type Burger de la mort (DB).")

        return value

    def create(self, validated_data):
        question_ids = validated_data.pop("question_ids", [])
        with transaction.atomic():
            deadly_burger = DeadlyBurger.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                DeadlyBurgerQuestion.objects.create(deadly_burger=deadly_burger, question_id=qid, order=order)
        return deadly_burger

    def update(self, instance, validated_data):
        question_ids = validated_data.pop("question_ids", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    DeadlyBurgerQuestion.objects.create(deadly_burger=instance, question_id=qid, order=order)
        return instance
