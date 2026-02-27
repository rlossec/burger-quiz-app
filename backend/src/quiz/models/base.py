"""
Mixins réutilisables pour les modèles quiz.
"""

from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager

from .tags import UUIDTaggedItem


class TimestampMixin(models.Model):
    """Mixin ajoutant created_at et updated_at."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthoredMixin(models.Model):
    """Mixin ajoutant un champ author (ForeignKey vers CustomUser)."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_authored",
        verbose_name="auteur",
    )

    class Meta:
        abstract = True


class TaggedMixin(models.Model):
    """Mixin ajoutant les tags via django-taggit avec support UUID."""

    tags = TaggableManager(through=UUIDTaggedItem, blank=True, verbose_name="tags")

    class Meta:
        abstract = True


class QuizContentMixin(TimestampMixin, AuthoredMixin, TaggedMixin):
    """
    Mixin combiné pour le contenu quiz.
    Inclut : created_at, updated_at, author, tags.
    """

    class Meta:
        abstract = True
