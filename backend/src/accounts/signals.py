from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def remember_old_avatar_name(sender, instance, **kwargs):
    """Mémorise le nom du fichier avatar à retirer du stockage si remplacé ou effacé."""
    if not instance.pk:
        return
    try:
        old = CustomUser.objects.get(pk=instance.pk)
    except CustomUser.DoesNotExist:
        return
    old_name = old.avatar.name or ""
    new_name = instance.avatar.name or ""
    if old_name and old_name != new_name:
        instance._old_avatar_name_to_delete = old_name


@receiver(post_save, sender=CustomUser)
def delete_old_avatar_file(sender, instance, **kwargs):
    """Supprime l'ancien fichier média après mise à jour du champ avatar."""
    name = getattr(instance, "_old_avatar_name_to_delete", None)
    if not name:
        return
    delattr(instance, "_old_avatar_name_to_delete")
    default_storage.delete(name)
