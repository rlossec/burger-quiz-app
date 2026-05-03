"""
Schémas OpenAPI (inline_serializer) pour @extend_schema sur le UserViewSet Djoser.

Alignés sur les sérialiseurs configurés dans DJOSER['SERIALIZERS'] (pas d'activation
de *_RETYPE sur set_password / reset_password_confirm dans ce projet).

Les formulaires JWT proviennent de rest_framework_simplejwt (routes ``jwt/create/``,
etc.) : utiles si vous enveloppez ces vues avec extend_schema.
"""

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

# --- Suppression de compte (UserDeleteSerializer) ---

DeleteUserDoc = inline_serializer(
    name="DeleteUserRequest",
    fields={
        "current_password": serializers.CharField(
            help_text="Mot de passe actuel — requis pour confirmer la suppression"
        ),
    },
)
# --- set_password : SetPasswordSerializer (sans re-saisie) ---

SetPasswordDoc = inline_serializer(
    name="SetPasswordRequest",
    fields={
        "current_password": serializers.CharField(help_text="Mot de passe actuel."),
        "new_password": serializers.CharField(help_text="Nouveau mot de passe."),
    },
)

# --- set_username : SetUsernameSerializer ---

SetUsernameDoc = inline_serializer(
    name="SetUsernameRequest",
    fields={
        "current_password": serializers.CharField(help_text="Mot de passe actuel."),
        "new_username": serializers.CharField(help_text="Nouveau nom d'utilisateur."),
    },
)

# --- reset_password : SendEmailResetSerializer ---

ResetPasswordDoc = inline_serializer(
    name="ResetPasswordRequest",
    fields={
        "email": serializers.EmailField(help_text="Adresse e-mail liée au compte."),
    },
)

# --- reset_password_confirm : PasswordResetConfirmSerializer (sans re-saisie) ---

ResetPasswordConfirmDoc = inline_serializer(
    name="ResetPasswordConfirmRequest",
    fields={
        "uid": serializers.CharField(help_text="UID reçu par e-mail."),
        "token": serializers.CharField(help_text="Token reçu par e-mail."),
        "new_password": serializers.CharField(help_text="Nouveau mot de passe."),
    },
)

# --- JWT SimpleJWT (documentation optionnelle hors UserViewSet) ---

JwtCreateDoc = inline_serializer(
    name="JWTCreateRequest",
    fields={
        "username": serializers.CharField(help_text="Identifiant (USERNAME_FIELD)."),
        "password": serializers.CharField(help_text="Mot de passe.", write_only=True),
    },
)

JwtRefreshDoc = inline_serializer(
    name="JWTRefreshRequest",
    fields={
        "refresh": serializers.CharField(help_text="Jeton refresh."),
    },
)

JwtVerifyDoc = inline_serializer(
    name="JWTVerifyRequest",
    fields={
        "token": serializers.CharField(help_text="Jeton access à vérifier."),
    },
)
