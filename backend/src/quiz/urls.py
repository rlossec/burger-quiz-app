from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    QuestionViewSet,
    NuggetsViewSet,
    SaltOrPepperViewSet,
    MenusViewSet,
    MenuThemeViewSet,
)

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")
router.register("nuggets", NuggetsViewSet, basename="nuggets")
router.register("salt-or-pepper", SaltOrPepperViewSet, basename="salt-or-pepper")
router.register("menus", MenusViewSet, basename="menus")
router.register("menu-theme", MenuThemeViewSet, basename="menu-theme")

urlpatterns = [
    path("quiz/", include(router.urls)),
]
