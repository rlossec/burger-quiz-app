# Factories avec factory_boy pour les données de test du module quiz.

import factory
from factory.django import DjangoModelFactory

from ..models import (
    Question,
    Answer,
    Nuggets,
    NuggetQuestion,
    SaltOrPepper,
    MenuTheme,
    MenuThemeQuestion,
    Menus,
    Addition,
    AdditionQuestion,
    DeadlyBurger,
    DeadlyBurgerQuestion,
    BurgerQuiz,
)
from . import (
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
    MENU_TYPE_CL,
    MENU_TYPE_TR,
)


# ---------------------------------------------------------------------------
# Question & Answer
# ---------------------------------------------------------------------------


class QuestionFactory(DjangoModelFactory):
    """Factory de base pour Question. Utiliser les sous-classes ou .create(question_type=...)."""

    class Meta:
        model = Question

    text = factory.Sequence(lambda n: f"Question {n}")
    question_type = QUESTION_TYPE_NU
    original = False

    @classmethod
    def create_nu(cls, text="Q NU", original=False, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_NU, original=original, **kwargs)

    @classmethod
    def create_sp(cls, text="Q SP", original=False, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_SP, original=original, **kwargs)

    @classmethod
    def create_me(cls, text="Q ME", original=False, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_ME, original=original, **kwargs)

    @classmethod
    def create_ad(cls, text="Q AD", original=False, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_AD, original=original, **kwargs)

    @classmethod
    def create_db(cls, text="Q DB", original=False, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_DB, original=original, **kwargs)

    @classmethod
    def create_nu_with_answers(cls, text="Q NU avec réponses", correct_index=2, **kwargs):
        q = cls.create_nu(text=text, **kwargs)
        for i in range(4):
            AnswerFactory.create(
                question=q,
                text=f"Réponse {chr(65 + i)}",
                is_correct=(i == correct_index),
            )
        return q


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    text = factory.Sequence(lambda n: f"Réponse {n}")
    is_correct = False


# ---------------------------------------------------------------------------
# Nuggets (M2M through NuggetQuestion)
# ---------------------------------------------------------------------------


class NuggetsFactory(DjangoModelFactory):
    class Meta:
        model = Nuggets

    title = factory.Sequence(lambda n: f"Culture générale {n}")
    original = False

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            NuggetQuestion.objects.create(nuggets=obj, question=q, order=order)


# ---------------------------------------------------------------------------
# SaltOrPepper (M2M through SaltOrPepperQuestion)
# ---------------------------------------------------------------------------


class SaltOrPepperFactory(DjangoModelFactory):
    class Meta:
        model = SaltOrPepper

    title = factory.Sequence(lambda n: f"Noir ou Blanc {n}")
    choice_labels = ["Noir", "Blanc"]
    original = False
    description = ""

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        from ..models import SaltOrPepperQuestion
        for order, q in enumerate(extracted):
            SaltOrPepperQuestion.objects.create(
                salt_or_pepper=obj, question=q, order=order
            )


# ---------------------------------------------------------------------------
# MenuTheme (M2M through MenuThemeQuestion)
# ---------------------------------------------------------------------------


class MenuThemeFactory(DjangoModelFactory):
    class Meta:
        model = MenuTheme

    title = factory.Sequence(lambda n: f"Thème {n}")
    type = MENU_TYPE_CL

    @factory.post_generation
    def question_ids(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            MenuThemeQuestion.objects.create(
                menu_theme=obj, question=q, order=order
            )

    @classmethod
    def create_classic(cls, title="Thème classique", question_ids=None, **kwargs):
        inst = cls.create(title=title, type=MENU_TYPE_CL, **kwargs)
        if question_ids:
            for order, q in enumerate(question_ids):
                MenuThemeQuestion.objects.create(
                    menu_theme=inst, question=q, order=order
                )
        return inst

    @classmethod
    def create_troll(cls, title="Thème troll", question_ids=None, **kwargs):
        inst = cls.create(title=title, type=MENU_TYPE_TR, **kwargs)
        if question_ids:
            for order, q in enumerate(question_ids):
                MenuThemeQuestion.objects.create(
                    menu_theme=inst, question=q, order=order
                )
        return inst


# ---------------------------------------------------------------------------
# Menus (FKs menu_1, menu_2, menu_troll)
# ---------------------------------------------------------------------------


class MenusFactory(DjangoModelFactory):
    class Meta:
        model = Menus

    title = factory.Sequence(lambda n: f"Menus du jour {n}")
    original = False
    description = ""
    menu_1 = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_CL)
    menu_2 = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_CL)
    menu_troll = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_TR)


# ---------------------------------------------------------------------------
# Addition (M2M through AdditionQuestion)
# ---------------------------------------------------------------------------


class AdditionFactory(DjangoModelFactory):
    class Meta:
        model = Addition

    title = factory.Sequence(lambda n: f"Addition rapide {n}")
    original = False
    description = ""

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            AdditionQuestion.objects.create(
                addition=obj, question=q, order=order
            )


# ---------------------------------------------------------------------------
# DeadlyBurger (M2M through DeadlyBurgerQuestion)
# ---------------------------------------------------------------------------


class DeadlyBurgerFactory(DjangoModelFactory):
    class Meta:
        model = DeadlyBurger

    title = factory.Sequence(lambda n: f"Burger de la mort {n}")
    original = False

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            DeadlyBurgerQuestion.objects.create(
                deadly_burger=obj, question=q, order=order
            )

    @classmethod
    def create_with_ten_questions(cls, title="Burger de la mort - Finale", **kwargs):
        questions = [
            QuestionFactory.create_db(text=f"DB{i}") for i in range(1, 11)
        ]
        return cls.create(title=title, questions=questions, **kwargs)


# ---------------------------------------------------------------------------
# BurgerQuiz (FKs optionnels)
# ---------------------------------------------------------------------------


class BurgerQuizFactory(DjangoModelFactory):
    class Meta:
        model = BurgerQuiz

    title = factory.Sequence(lambda n: f"Session test {n}")
    toss = "Consigne du toss."
    nuggets = None
    salt_or_pepper = None
    menus = None
    addition = None
    deadly_burger = None

    @classmethod
    def create_full(cls, title="Session complète", toss="Toss complet", **kwargs):
        """Burger Quiz avec toutes les manches créées automatiquement."""
        return cls.create(
            title=title,
            toss=toss,
            nuggets=NuggetsFactory.create(),
            salt_or_pepper=SaltOrPepperFactory.create(),
            menus=MenusFactory.create(),
            addition=AdditionFactory.create(),
            deadly_burger=DeadlyBurgerFactory.create(),
            **kwargs,
        )
