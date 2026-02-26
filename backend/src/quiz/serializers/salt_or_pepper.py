from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import SaltOrPepper, Question
from ..models.enums import QuestionType
from ..models.salt_or_pepper import SaltOrPepperQuestion


class SaltOrPepperSerializer(ModelSerializer):
    propositions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
    )
    question_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
    )
    questions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SaltOrPepper
        fields = ["id", "title", "description", "original", "propositions", "questions", "question_ids"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "title": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    def get_questions(self, obj):
        return [str(q.id) for q in obj.questions.all()]

    def validate_propositions(self, value):
        if value is None:
            return value

        # Entre 2 et 5 propositions
        if len(value) < 2:
            raise serializers.ValidationError("Il faut au moins 2 propositions.")
        if len(value) > 5:
            raise serializers.ValidationError("Il ne peut y avoir plus de 5 propositions.")

        # Pas de doublons
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Les propositions ne doivent pas contenir de doublons.")

        return value

    def validate(self, attrs):
        # À la création, propositions est obligatoire
        if self.instance is None and "propositions" not in attrs:
            raise serializers.ValidationError({"propositions": "Ce champ est obligatoire."})
        return attrs

    def to_representation(self, instance):
        """En lecture, expose 'propositions' à la place de 'choice_labels'."""
        ret = super().to_representation(instance)
        ret["propositions"] = instance.choice_labels
        return ret

    def validate_question_ids(self, value):
        if value is None:
            return value

        # Vérifier que toutes les questions existent et sont de type SP
        questions = Question.objects.filter(id__in=value)
        if questions.count() != len(value):
            raise serializers.ValidationError("Une ou plusieurs questions n'existent pas.")

        non_sp_questions = questions.exclude(question_type=QuestionType.SP)
        if non_sp_questions.exists():
            raise serializers.ValidationError("Toutes les questions doivent être de type Sel ou Poivre (SP).")

        return value

    def create(self, validated_data):
        propositions = validated_data.pop("propositions")
        question_ids = validated_data.pop("question_ids", [])
        validated_data["choice_labels"] = propositions

        with transaction.atomic():
            sop = SaltOrPepper.objects.create(**validated_data)
            for order, qid in enumerate(question_ids):
                SaltOrPepperQuestion.objects.create(salt_or_pepper=sop, question_id=qid, order=order)
        return sop

    def update(self, instance, validated_data):
        propositions = validated_data.pop("propositions", None)
        question_ids = validated_data.pop("question_ids", None)

        if propositions is not None:
            validated_data["choice_labels"] = propositions

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if question_ids is not None:
                instance.questions.clear()
                for order, qid in enumerate(question_ids):
                    SaltOrPepperQuestion.objects.create(salt_or_pepper=instance, question_id=qid, order=order)
        return instance
