from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Addition, Question
from ..models.enums import QuestionType
from ..models.addition import AdditionQuestion


class AdditionSerializer(ModelSerializer):
    questions = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Addition
        fields = ["id", "title", "description", "original", "questions", "question_ids"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
            "original": {"required": False},
        }

    def validate(self, attrs):
        question_ids = attrs.pop("question_ids", None)
        if question_ids is not None:
            attrs["questions"] = question_ids

        questions = attrs.get("questions")
        if questions is not None:
            # Pas de doublons
            if len(questions) != len(set(questions)):
                raise serializers.ValidationError({"questions": "Les IDs de questions ne doivent pas être dupliqués."})

            # Vérifier que toutes les questions existent
            existing_questions = Question.objects.filter(id__in=questions)
            if existing_questions.count() != len(questions):
                raise serializers.ValidationError({"questions": "Les IDs de questions ne doivent pas être inexistants."})

            # Vérifier que toutes les questions sont de type AD
            non_ad_questions = existing_questions.exclude(question_type=QuestionType.AD)
            if non_ad_questions.exists():
                raise serializers.ValidationError({"questions": "Toutes les questions doivent être de type Addition (AD)."})

        return attrs

    def create(self, validated_data):
        question_ids = validated_data.pop("questions", [])
        with transaction.atomic():
            addition = Addition.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                AdditionQuestion.objects.create(addition=addition, question_id=qid, order=order)
        return addition

    def update(self, instance, validated_data):
        question_ids = validated_data.pop("questions", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    AdditionQuestion.objects.create(addition=instance, question_id=qid, order=order)
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ordered_questions = AdditionQuestion.objects.filter(addition=instance).order_by("order")
        ret["questions"] = [str(aq.question_id) for aq in ordered_questions]
        return ret
