from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import MenuTheme, Question
from ..models.enums import QuestionType
from ..models.menu import MenuThemeQuestion


class MenuThemeSerializer(ModelSerializer):
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)
    type = serializers.ChoiceField(
        choices=MenuTheme.MENU_TYPES,
        error_messages={"required": "Ce champ est obligatoire."},
    )

    class Meta:
        model = MenuTheme
        fields = ["id", "title", "type", "original", "questions", "question_ids"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    def get_questions(self, obj):
        return [str(q.id) for q in obj.questions.all()]

    def validate_question_ids(self, value):
        if value is None:
            return value

        # Vérifier que toutes les questions existent et sont de type ME
        questions = Question.objects.filter(id__in=value)
        if questions.count() != len(value):
            raise serializers.ValidationError("Une ou plusieurs questions n'existent pas.")

        non_me_questions = questions.exclude(question_type=QuestionType.ME)
        if non_me_questions.exists():
            raise serializers.ValidationError("Toutes les questions doivent être de type Menu (ME).")

        return value

    def create(self, validated_data):
        question_ids = validated_data.pop("question_ids", [])
        with transaction.atomic():
            menu_theme = MenuTheme.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                MenuThemeQuestion.objects.create(menu_theme=menu_theme, question_id=qid, order=order)
        return menu_theme

    def update(self, instance, validated_data):
        question_ids = validated_data.pop("question_ids", None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    MenuThemeQuestion.objects.create(menu_theme=instance, question_id=qid, order=order)
        return instance
