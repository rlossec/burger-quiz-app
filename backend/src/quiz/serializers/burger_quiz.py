from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer

from ..models import BurgerQuiz
from .base import AuthorSerializer
from .structure import structure_elements_to_representation


class BurgerQuizSerializer(TaggitSerializer, ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)
    structure = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BurgerQuiz
        fields = [
            "id",
            "title",
            "toss",
            "author",
            "tags",
            "created_at",
            "updated_at",
            "structure",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "updated_at",
            "structure",
        ]
        extra_kwargs = {
            "toss": {"error_messages": {"required": "Ce champ est obligatoire.", "blank": "Ce champ ne peut pas être vide."}},
        }

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_structure(self, obj):
        request = self.context.get("request")
        expand_full = bool(request and request.query_params.get("expand") == "full")
        return structure_elements_to_representation(obj, expand_full=expand_full)

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
