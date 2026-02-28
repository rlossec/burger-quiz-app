import uuid

from django.db import models

from .enums import ElementType, QuestionType


class BurgerQuizElement(models.Model):
    """
    Élément ordonné dans la structure d'un Burger Quiz.
    Peut être une manche (round) ou un interlude vidéo.
    """

    class Meta:
        verbose_name = "Élément de Burger Quiz"
        verbose_name_plural = "Éléments de Burger Quiz"
        ordering = ["burger_quiz", "order"]
        unique_together = [
            ("burger_quiz", "order"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    burger_quiz = models.ForeignKey(
        "BurgerQuiz",
        on_delete=models.CASCADE,
        related_name="structure_elements",
        verbose_name="Burger Quiz",
    )
    order = models.PositiveIntegerField(verbose_name="Ordre")
    element_type = models.CharField(
        max_length=10,
        choices=ElementType.choices,
        verbose_name="Type d'élément",
    )
    round_type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
        null=True,
        blank=True,
        verbose_name="Type de manche",
    )
    interlude = models.ForeignKey(
        "VideoInterlude",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="burger_quiz_elements",
        verbose_name="Interlude",
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.element_type == ElementType.ROUND:
            if not self.round_type:
                raise ValidationError(
                    {"round_type": "Le type de manche est requis pour un élément de type 'round'."}
                )
            if self.interlude:
                raise ValidationError(
                    {"interlude": "Un élément de type 'round' ne peut pas avoir d'interlude."}
                )
        elif self.element_type == ElementType.INTERLUDE:
            if not self.interlude:
                raise ValidationError(
                    {"interlude": "Un interlude est requis pour un élément de type 'interlude'."}
                )
            if self.round_type:
                raise ValidationError(
                    {"round_type": "Un élément de type 'interlude' ne peut pas avoir de type de manche."}
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.element_type == ElementType.ROUND:
            return f"#{self.order} Manche {self.round_type}"
        return f"#{self.order} Interlude: {self.interlude}"

    def __repr__(self):
        return f"<BurgerQuizElement {self.burger_quiz_id} #{self.order} {self.element_type}>"
