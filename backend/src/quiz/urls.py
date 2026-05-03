from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    QuestionViewSet,
    NuggetsViewSet,
    SaltOrPepperViewSet,
    MenusViewSet,
    MenuThemeViewSet,
    AdditionViewSet,
    DeadlyBurgerViewSet,
    VideoInterludeViewSet,
    BurgerQuizViewSet,
)

router = DefaultRouter()
router.register("interludes", VideoInterludeViewSet, basename="interlude")
router.register("questions", QuestionViewSet, basename="question")
router.register("nuggets", NuggetsViewSet, basename="nuggets")
router.register("salt-or-pepper", SaltOrPepperViewSet, basename="salt-or-pepper")
router.register("menus", MenusViewSet, basename="menus")
router.register("menu-theme", MenuThemeViewSet, basename="menu-theme")
router.register("additions", AdditionViewSet, basename="addition")
router.register("deadly-burgers", DeadlyBurgerViewSet, basename="deadly-burger")
router.register("burger-quizzes", BurgerQuizViewSet, basename="burger-quiz")

urlpatterns = [
    path("quiz/", include(router.urls)),
]
