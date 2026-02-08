from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """Gestionnaire personnalisé utilisant l'email comme identifiant."""

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être renseignée.")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        return super().create_user(username=email, email=email, password=password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être renseignée.")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        return super().create_superuser(username=email, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé héritant d'AbstractUser.
    Utilise l'email comme identifiant principal à la place du username.
    """

    email = models.EmailField("adresse email", unique=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.email
