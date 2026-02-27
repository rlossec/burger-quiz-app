"""
Modèle TaggedItem personnalisé pour supporter les UUID comme clé primaire.
"""

from django.db import models
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    """
    TaggedItem personnalisé utilisant un UUIDField pour object_id.
    Nécessaire car nos modèles utilisent des UUID comme clé primaire.
    
    Hérite de GenericUUIDTaggedItemBase qui définit object_id comme UUIDField,
    et de TaggedItemBase qui fournit le champ tag.
    """

    class Meta:
        verbose_name = "tagged item"
        verbose_name_plural = "tagged items"
