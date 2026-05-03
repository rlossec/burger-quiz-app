"""
Mixins réutilisables pour les serializers quiz.
"""

from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer


class AuthorSerializer(serializers.Serializer):
    """Serializer minimal pour l'auteur (lecture seule)."""

    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)


class AuthorTagSerializerMixin(TaggitSerializer, serializers.Serializer):
    """
    Mixin pour ajouter author et tags aux serializers.
    - author : lecture seule, affiché avec id et username
    - tags : liste de chaînes, lecture/écriture
    """

    author = AuthorSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    def get_author_tag_fields(self):
        """Retourne les champs à ajouter au Meta.fields."""
        return ["author", "tags", "created_at", "updated_at"]

    def get_author_tag_read_only_fields(self):
        """Retourne les champs read_only à ajouter."""
        return ["author", "created_at", "updated_at"]
