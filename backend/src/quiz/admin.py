"""
Configuration du portail admin pour l'app quiz.

Organisation : Questions/Réponses → Manches (Nuggets, Sel ou Poivre, etc.) → Burger Quiz.
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Addition,
    AdditionQuestion,
    Answer,
    BurgerQuiz,
    DeadlyBurger,
    DeadlyBurgerQuestion,
    MenuTheme,
    MenuThemeQuestion,
    Menus,
    NuggetQuestion,
    Nuggets,
    Question,
    SaltOrPepper,
    SaltOrPepperQuestion,
)
from .models.enums import QuestionType


# ========== Réponses ==========


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    ordering = ["pk"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text_preview", "question_preview", "is_correct")
    list_filter = ("is_correct", "question__question_type")
    search_fields = ("text", "question__text")
    list_select_related = ("question",)
    autocomplete_fields = ["question"]
    list_per_page = 25

    @admin.display(description="Réponse")
    def text_preview(self, obj):
        return obj.text[:60] + "…" if len(obj.text) > 60 else obj.text

    @admin.display(description="Question")
    def question_preview(self, obj):
        return obj.question.text[:50] + "…" if len(obj.question.text) > 50 else obj.question.text


# ========== Questions ==========


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_preview", "question_type", "order", "answers_count")
    list_filter = ("question_type",)
    search_fields = ("text", "explanations")
    ordering = ["order", "text"]
    inlines = [AnswerInline]
    list_editable = ["order"]
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("text", "question_type", "order")}),
        ("Explications", {"fields": ("explanations",), "classes": ("collapse",)}),
    )

    @admin.display(description="Question")
    def text_preview(self, obj):
        return obj.text[:60] + "…" if len(obj.text) > 60 else obj.text

    @admin.display(description="Réponses")
    def answers_count(self, obj):
        count = obj.answers.count()
        return format_html('<strong>{}</strong>', count)


# ========== Manches - Modèles intermédiaires ==========


class NuggetQuestionInline(admin.TabularInline):
    model = NuggetQuestion
    extra = 1
    ordering = ["order"]
    autocomplete_fields = ["question"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type=QuestionType.NU)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SaltOrPepperQuestionInline(admin.TabularInline):
    model = SaltOrPepperQuestion
    extra = 1
    ordering = ["order"]
    autocomplete_fields = ["question"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type=QuestionType.SP)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MenuThemeQuestionInline(admin.TabularInline):
    model = MenuThemeQuestion
    extra = 1
    ordering = ["order"]
    autocomplete_fields = ["question"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type=QuestionType.ME)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AdditionQuestionInline(admin.TabularInline):
    model = AdditionQuestion
    extra = 1
    ordering = ["order"]
    autocomplete_fields = ["question"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type=QuestionType.AD)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DeadlyBurgerQuestionInline(admin.TabularInline):
    model = DeadlyBurgerQuestion
    extra = 1
    ordering = ["order"]
    autocomplete_fields = ["question"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type=QuestionType.DB)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ========== Manches ==========


@admin.register(Nuggets)
class NuggetsAdmin(admin.ModelAdmin):
    list_display = ("title", "questions_count")
    search_fields = ("title",)
    inlines = [NuggetQuestionInline]
    list_per_page = 25

    @admin.display(description="Questions")
    def questions_count(self, obj):
        return obj.questions.count()


@admin.register(SaltOrPepper)
class SaltOrPepperAdmin(admin.ModelAdmin):
    list_display = ("title", "description_preview", "questions_count")
    search_fields = ("title", "description")
    inlines = [SaltOrPepperQuestionInline]
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("title", "description")}),
    )

    @admin.display(description="Description")
    def description_preview(self, obj):
        if not obj.description:
            return "—"
        return obj.description[:40] + "…" if len(obj.description) > 40 else obj.description

    @admin.display(description="Questions")
    def questions_count(self, obj):
        return obj.questions.count()


@admin.register(MenuTheme)
class MenuThemeAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "questions_count")
    list_filter = ("type",)
    search_fields = ("title",)
    inlines = [MenuThemeQuestionInline]
    list_per_page = 25

    @admin.display(description="Questions")
    def questions_count(self, obj):
        return obj.questions.count()


@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ("title", "menu_1", "menu_2", "menu_troll", "description_preview")
    list_filter = ("menu_1", "menu_2", "menu_troll")
    search_fields = ("title", "description")
    autocomplete_fields = ["menu_1", "menu_2", "menu_troll"]
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("Menus", {"fields": ("menu_1", "menu_2", "menu_troll")}),
    )

    @admin.display(description="Description")
    def description_preview(self, obj):
        if not obj.description:
            return "—"
        return obj.description[:40] + "…" if len(obj.description) > 40 else obj.description


@admin.register(Addition)
class AdditionAdmin(admin.ModelAdmin):
    list_display = ("title", "description_preview", "questions_count")
    search_fields = ("title", "description")
    inlines = [AdditionQuestionInline]
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("title", "description")}),
    )

    @admin.display(description="Description")
    def description_preview(self, obj):
        if not obj.description:
            return "—"
        return obj.description[:40] + "…" if len(obj.description) > 40 else obj.description

    @admin.display(description="Questions")
    def questions_count(self, obj):
        return obj.questions.count()


@admin.register(DeadlyBurger)
class DeadlyBurgerAdmin(admin.ModelAdmin):
    list_display = ("title", "questions_count")
    search_fields = ("title",)
    inlines = [DeadlyBurgerQuestionInline]
    list_per_page = 25

    @admin.display(description="Questions")
    def questions_count(self, obj):
        return obj.questions.count()


# ========== Burger Quiz ==========


@admin.register(BurgerQuiz)
class BurgerQuizAdmin(admin.ModelAdmin):
    list_display = ("title", "nuggets", "salt_or_pepper", "menus", "addition", "deadly_burger")
    list_filter = ("nuggets", "menus", "addition", "deadly_burger")
    search_fields = ("title", "toss")
    autocomplete_fields = ["nuggets", "salt_or_pepper", "menus", "addition", "deadly_burger"]
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("title", "toss")}),
        ("Manches", {
            "fields": ("nuggets", "salt_or_pepper", "menus", "addition", "deadly_burger"),
            "description": "Associer une manche à chaque étape du quiz.",
        }),
    )
