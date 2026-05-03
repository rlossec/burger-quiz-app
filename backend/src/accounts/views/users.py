from djoser import views as djoser_views
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.pagination import PageNumberPagination

from ..serializers.docs import (
    DeleteUserDoc,
    ResetPasswordConfirmDoc,
    ResetPasswordDoc,
    SetPasswordDoc,
    SetUsernameDoc,
)
from .jwt import TAG_AUTHENTIFICATION

TAG_COMPTE = "Compte personnel"
TAG_ADMIN = "Utilisateurs — administration"


class UserListPagination(PageNumberPagination):
    """Pagination limitée à la liste des utilisateurs."""

    page_size = 10


@extend_schema_view(
    create=extend_schema(
        description="Inscription d'un nouvel utilisateur.",
        tags=[TAG_AUTHENTIFICATION],
    ),
    list=extend_schema(
        description="Liste des utilisateurs",
        tags=[TAG_ADMIN],
    ),
    retrieve=extend_schema(
        description="Détail utilisateur",
        tags=[TAG_ADMIN],
    ),
    update=extend_schema(
        description="Mise à jour complète d'un utilisateur (par id)",
        tags=[TAG_ADMIN],
    ),
    partial_update=extend_schema(
        description="Mise à jour partielle d'un utilisateur (par id)",
        tags=[TAG_ADMIN],
    ),
    activation=extend_schema(
        description="Activation du compte utilisateur",
        tags=[TAG_AUTHENTIFICATION],
    ),
    resend_activation=extend_schema(
        description="Renvoyer l'e-mail d'activation",
        tags=[TAG_AUTHENTIFICATION],
    ),
    me=(
        extend_schema(
            methods=["GET"],
            description="Lecture du profil authentifié.",
            tags=[TAG_COMPTE],
        ),
        extend_schema(
            methods=["PUT"],
            description="Mise à jour du profil authentifié.",
            tags=[TAG_COMPTE],
        ),
        extend_schema(
            methods=["PATCH"],
            description="Mise à jour partielle du profil authentifié.",
            tags=[TAG_COMPTE],
        ),
        extend_schema(
            methods=["DELETE"],
            description=(
                "Suppression définitive du compte courant. "
                "Corps JSON : mot de passe actuel (`current_password`)."
            ),
            request=DeleteUserDoc,
            responses={204: None},
            tags=[TAG_COMPTE],
        ),
    ),
    destroy=extend_schema(
        description=(
            "Suppression du compte identifié par `id`. "
            "Corps JSON : mot de passe actuel de l'appelant (`current_password`), comme Djoser."
        ),
        request=DeleteUserDoc,
        responses={204: None},
        tags=[TAG_ADMIN],
    ),
    set_password=extend_schema(
        description="Changement de mot de passe.",
        request=SetPasswordDoc,
        responses={204: None},
        tags=[TAG_COMPTE],
    ),
    set_username=extend_schema(
        description="Changement de nom d'utilisateur.",
        request=SetUsernameDoc,
        responses={204: None},
        tags=[TAG_COMPTE],
    ),
    reset_password=extend_schema(
        description="Demande de réinitialisation de mot de passe.",
        request=ResetPasswordDoc,
        responses={204: None},
        tags=[TAG_AUTHENTIFICATION],
    ),
    reset_password_confirm=extend_schema(
        description="Confirmation de la réinitialisation de mot de passe.",
        request=ResetPasswordConfirmDoc,
        responses={204: None},
        tags=[TAG_AUTHENTIFICATION],
    ),
    reset_username=extend_schema(
        description="Demande de réinitialisation du nom d'utilisateur.",
        tags=[TAG_AUTHENTIFICATION],
    ),
    reset_username_confirm=extend_schema(
        description="Confirmation de la réinitialisation du nom d'utilisateur.",
        tags=[TAG_AUTHENTIFICATION],
    ),
)
class UserViewSet(djoser_views.UserViewSet):
    pagination_class = UserListPagination
