from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    QuestionViewSet,
    NuggetsViewSet,
)

router = DefaultRouter()
router.register("questions", QuestionViewSet, basename="question")
router.register("nuggets", NuggetsViewSet, basename="nuggets")

urlpatterns = [
    path("quiz/", include(router.urls)),
]
