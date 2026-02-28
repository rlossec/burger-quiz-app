import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer

from ..models import VideoInterlude, InterludeType
from .base import AuthorSerializer


class VideoInterludeListSerializer(ModelSerializer):
    """Serializer pour la liste des interludes (champs minimaux)."""

    class Meta:
        model = VideoInterlude
        fields = [
            "id",
            "title",
            "youtube_url",
            "youtube_video_id",
            "interlude_type",
            "duration_seconds",
            "autoplay",
            "skip_allowed",
            "skip_after_seconds",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class VideoInterludeSerializer(TaggitSerializer, ModelSerializer):
    """Serializer complet pour les interludes vidéo."""

    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = VideoInterlude
        fields = [
            "id",
            "title",
            "youtube_url",
            "youtube_video_id",
            "interlude_type",
            "duration_seconds",
            "autoplay",
            "skip_allowed",
            "skip_after_seconds",
            "author",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "youtube_video_id",
            "author",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "title": {
                "error_messages": {
                    "required": "Ce champ est obligatoire.",
                    "blank": "Ce champ ne peut pas être vide.",
                }
            },
            "youtube_url": {
                "error_messages": {
                    "required": "Ce champ est obligatoire.",
                    "blank": "Ce champ ne peut pas être vide.",
                }
            },
            "interlude_type": {
                "required": False,
            },
        }

    YOUTUBE_PATTERNS = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]+)",
    ]

    def validate_youtube_url(self, value):
        """Valide que l'URL est une URL YouTube valide."""
        if not value:
            return value

        for pattern in self.YOUTUBE_PATTERNS:
            if re.search(pattern, value):
                return value

        raise serializers.ValidationError("L'URL YouTube n'est pas valide.")

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        instance = VideoInterlude.objects.create(**validated_data)
        if tags is not None:
            instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance


class VideoInterludeMinimalSerializer(ModelSerializer):
    """Serializer minimal pour inclusion dans d'autres réponses."""

    class Meta:
        model = VideoInterlude
        fields = [
            "id",
            "title",
            "interlude_type",
            "youtube_video_id",
        ]
        read_only_fields = fields
