from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
from .views.jwt import (
    AuthentificationTokenObtainPairView,
    AuthentificationTokenRefreshView,
    AuthentificationTokenVerifyView,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("jwt/create/", AuthentificationTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", AuthentificationTokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", AuthentificationTokenVerifyView.as_view(), name="jwt-verify"),
]
