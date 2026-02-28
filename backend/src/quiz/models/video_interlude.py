import re
import uuid

from django.db import models

from .base import QuizContentMixin
from .enums import InterludeType


class VideoInterlude(QuizContentMixin, models.Model):
    """
    Interlude vidéo (intro, outro, pub) intégrable dans un Burger Quiz.
    Les interludes sont des entités réutilisables.
    """

    class Meta:
        verbose_name = "Interlude vidéo"
        verbose_name_plural = "Interludes vidéo"
        ordering = ["-created_at"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name="Titre")
    youtube_url = models.URLField(verbose_name="URL YouTube")
    youtube_video_id = models.CharField(
        max_length=20,
        blank=True,
        editable=False,
        verbose_name="ID vidéo YouTube",
    )
    interlude_type = models.CharField(
        max_length=2,
        choices=InterludeType.choices,
        default=InterludeType.IL,
        verbose_name="Type d'interlude",
    )
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Durée (secondes)",
    )
    autoplay = models.BooleanField(default=True, verbose_name="Lecture automatique")
    skip_allowed = models.BooleanField(default=True, verbose_name="Skip autorisé")
    skip_after_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Skip après (secondes)",
    )

    YOUTUBE_PATTERNS = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]+)",
    ]

    def save(self, *args, **kwargs):
        self.youtube_video_id = self._extract_youtube_video_id(self.youtube_url)
        super().save(*args, **kwargs)

    def _extract_youtube_video_id(self, url: str) -> str:
        """Extrait l'ID de la vidéo YouTube depuis l'URL."""
        if not url:
            return ""
        for pattern in self.YOUTUBE_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""

    def __str__(self):
        return f"{self.get_interlude_type_display()}: {self.title}"

    def __repr__(self):
        return f"<VideoInterlude {self.interlude_type}: {self.title}>"
