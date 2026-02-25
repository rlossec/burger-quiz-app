from rest_framework.serializers import ModelSerializer

from ..models.answer import Answer


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "text", "is_correct"]
