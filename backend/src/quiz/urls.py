from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    QuestionViewSet,
    NuggetsViewSet,
    SaltOrPepperViewSet,
)

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")
router.register("nuggets", NuggetsViewSet, basename="nuggets")
router.register("salt-or-pepper", SaltOrPepperViewSet, basename="salt-or-pepper")

urlpatterns = [
    path("quiz/", include(router.urls)),
]
