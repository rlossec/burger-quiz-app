from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """Gestionnaire personnalisé pour CustomUser."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return super().create_superuser(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé héritant d'AbstractUser.
    Utilise le username pour la connexion (portail admin).
    """

    email = models.EmailField("adresse email", unique=True, blank=False)
    avatar = models.ImageField("avatar", upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username
