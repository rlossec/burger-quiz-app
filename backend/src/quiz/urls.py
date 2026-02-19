from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("questions", views.PlaceholderViewSet, basename="question")
router.register("nuggets", views.PlaceholderViewSet, basename="nuggets")
router.register("salt-or-pepper", views.PlaceholderViewSet, basename="salt-or-pepper")
router.register("menu-themes", views.PlaceholderViewSet, basename="menu-theme")
router.register("menus", views.PlaceholderViewSet, basename="menus")
router.register("additions", views.PlaceholderViewSet, basename="addition")
router.register("deadly-burgers", views.PlaceholderViewSet, basename="deadly-burger")
router.register("burger-quizzes", views.PlaceholderViewSet, basename="burger-quiz")

urlpatterns = [
    path("quiz/", include(router.urls)),
]
