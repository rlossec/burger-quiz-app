
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

TAG_AUTHENTIFICATION = "Authentification"


@extend_schema(tags=[TAG_AUTHENTIFICATION])
class AuthentificationTokenObtainPairView(TokenObtainPairView):
    """Login : obtention de la paire access / refresh."""


@extend_schema(tags=[TAG_AUTHENTIFICATION])
class AuthentificationTokenRefreshView(TokenRefreshView):
    """Rafraîchissement du token d'accès."""


@extend_schema(tags=[TAG_AUTHENTIFICATION])
class AuthentificationTokenVerifyView(TokenVerifyView):
    """Vérification d'un token."""
