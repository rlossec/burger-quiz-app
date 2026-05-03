"""
Modèle TaggedItem personnalisé pour supporter les UUID comme clé primaire.
"""

from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = "tagged item"
        verbose_name_plural = "tagged items"
