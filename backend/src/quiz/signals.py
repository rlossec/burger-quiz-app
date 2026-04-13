"""
Crée / met à jour une ligne `Round` pour chaque manche concrète (même UUID).
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    TYPE_ADDITION,
    TYPE_DEADLY_BURGER,
    TYPE_MENUS,
    TYPE_NUGGETS,
    TYPE_SALT_OR_PEPPER,
    Addition,
    DeadlyBurger,
    Menus,
    Nuggets,
    Round,
    SaltOrPepper,
)


def _ensure_round(instance, round_type: str, field: str):
    """Round.id = instance.id ; une seule liaison OneToOne non nulle."""
    data = {
        "round_type": round_type,
        "nuggets": None,
        "salt_or_pepper": None,
        "menus": None,
        "addition": None,
        "deadly_burger": None,
    }
    data[field] = instance
    Round.objects.update_or_create(id=instance.id, defaults=data)


@receiver(post_save, sender=Nuggets)
def round_from_nuggets(sender, instance, **kwargs):
    _ensure_round(instance, TYPE_NUGGETS.slug, TYPE_NUGGETS.round_fk)


@receiver(post_save, sender=SaltOrPepper)
def round_from_salt_or_pepper(sender, instance, **kwargs):
    _ensure_round(instance, TYPE_SALT_OR_PEPPER.slug, TYPE_SALT_OR_PEPPER.round_fk)


@receiver(post_save, sender=Menus)
def round_from_menus(sender, instance, **kwargs):
    _ensure_round(instance, TYPE_MENUS.slug, TYPE_MENUS.round_fk)


@receiver(post_save, sender=Addition)
def round_from_addition(sender, instance, **kwargs):
    _ensure_round(instance, TYPE_ADDITION.slug, TYPE_ADDITION.round_fk)


@receiver(post_save, sender=DeadlyBurger)
def round_from_deadly_burger(sender, instance, **kwargs):
    _ensure_round(instance, TYPE_DEADLY_BURGER.slug, TYPE_DEADLY_BURGER.round_fk)
