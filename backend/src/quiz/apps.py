from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = "quiz"
    label = "quiz"
    verbose_name = "Quiz Burger"

    def ready(self):
        from . import signals  # noqa: F401
