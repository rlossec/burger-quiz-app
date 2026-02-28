# Factories avec factory_boy pour les données de test du module quiz.

import factory
from django.contrib.auth import get_user_model
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
    VideoInterlude,
    BurgerQuizElement,
)
from . import (
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
    MENU_TYPE_CL,
    MENU_TYPE_TR,
    INTERLUDE_TYPE_IN,
    INTERLUDE_TYPE_OU,
    INTERLUDE_TYPE_PU,
    INTERLUDE_TYPE_IL,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# User Factory (pour les tests d'auteur)
# ---------------------------------------------------------------------------


class UserFactory(DjangoModelFactory):
    """Factory pour créer des utilisateurs de test."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "TestPassword123!")

    @classmethod
    def create_author(cls, username="author", **kwargs):
        """Crée un utilisateur destiné à être auteur de contenu."""
        return cls.create(username=username, **kwargs)


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
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags à la question si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @classmethod
    def create_nu(cls, text="Q NU", original=False, author=None, tags=None, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_NU, original=original, author=author, tags=tags, **kwargs)

    @classmethod
    def create_sp(cls, text="Q SP", original=False, author=None, tags=None, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_SP, original=original, author=author, tags=tags, **kwargs)

    @classmethod
    def create_me(cls, text="Q ME", original=False, author=None, tags=None, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_ME, original=original, author=author, tags=tags, **kwargs)

    @classmethod
    def create_ad(cls, text="Q AD", original=False, author=None, tags=None, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_AD, original=original, author=author, tags=tags, **kwargs)

    @classmethod
    def create_db(cls, text="Q DB", original=False, author=None, tags=None, **kwargs):
        return cls.create(text=text, question_type=QUESTION_TYPE_DB, original=original, author=author, tags=tags, **kwargs)

    @classmethod
    def create_nu_with_answers(cls, text="Q NU avec réponses", correct_index=2, author=None, tags=None, **kwargs):
        q = cls.create_nu(text=text, author=author, tags=tags, **kwargs)
        for i in range(4):
            AnswerFactory.create(
                question=q,
                text=f"Réponse {chr(65 + i)}",
                is_correct=(i == correct_index),
            )
        return q

    @classmethod
    def create_batch_nu(cls, count, author=None, tags=None, **kwargs):
        """Crée un batch de questions Nuggets avec réponses."""
        questions = []
        for i in range(count):
            q = cls.create_nu_with_answers(
                text=f"Question NU {i + 1}",
                correct_index=i % 4,
                author=author,
                tags=tags,
                **kwargs,
            )
            questions.append(q)
        return questions

    @classmethod
    def create_sp_with_answers(cls, text="Q SP avec réponses", propositions=None, correct_index=0, author=None, tags=None, **kwargs):
        """Crée une question SP avec des réponses basées sur les propositions."""
        if propositions is None:
            propositions = ["Noir", "Blanc"]
        q = cls.create_sp(text=text, author=author, tags=tags, **kwargs)
        for i, prop in enumerate(propositions):
            AnswerFactory.create(
                question=q,
                text=prop,
                is_correct=(i == correct_index),
            )
        return q

    @classmethod
    def create_batch_sp(cls, count, propositions=None, author=None, tags=None, **kwargs):
        """Crée un batch de questions Sel ou Poivre avec réponses."""
        if propositions is None:
            propositions = ["Noir", "Blanc"]
        questions = []
        for i in range(count):
            q = cls.create_sp_with_answers(
                text=f"Question SP {i + 1}",
                propositions=propositions,
                correct_index=i % len(propositions),
                author=author,
                tags=tags,
                **kwargs,
            )
            questions.append(q)
        return questions

    @classmethod
    def create_ad_with_answer(cls, text="Q AD avec réponse", answer_text="42", author=None, tags=None, **kwargs):
        """Crée une question Addition avec une réponse."""
        q = cls.create_ad(text=text, author=author, tags=tags, **kwargs)
        AnswerFactory.create(question=q, text=answer_text, is_correct=True)
        return q

    @classmethod
    def create_batch_ad(cls, count, author=None, tags=None, **kwargs):
        """Crée un batch de questions Addition avec réponses."""
        questions = []
        for i in range(count):
            q = cls.create_ad_with_answer(
                text=f"Question AD {i + 1}",
                answer_text=str(i + 1),
                author=author,
                tags=tags,
                **kwargs,
            )
            questions.append(q)
        return questions

    @classmethod
    def create_batch_db(cls, count, author=None, tags=None, **kwargs):
        """Crée un batch de questions Burger de la mort (sans réponses)."""
        questions = []
        for i in range(count):
            q = cls.create_db(
                text=f"Question DB {i + 1}",
                author=author,
                tags=tags,
                **kwargs,
            )
            questions.append(q)
        return questions


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
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags aux nuggets si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            NuggetQuestion.objects.create(nuggets=obj, question=q, order=order)

    @classmethod
    def create_with_questions(cls, title="Nuggets avec questions", questions=None, author=None, tags=None, **kwargs):
        """Crée une manche Nuggets avec des questions."""
        if questions is None:
            questions = QuestionFactory.create_batch_nu(4)
        return cls.create(title=title, questions=questions, author=author, tags=tags, **kwargs)


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
    author = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override pour gérer le paramètre propositions."""
        propositions = kwargs.pop("propositions", None)
        if propositions is not None:
            kwargs["choice_labels"] = propositions
        return super()._create(model_class, *args, **kwargs)

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags au sel ou poivre si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        from ..models import SaltOrPepperQuestion
        for order, q in enumerate(extracted):
            SaltOrPepperQuestion.objects.create(
                salt_or_pepper=obj, question=q, order=order
            )

    @classmethod
    def create_with_questions(cls, title="SP avec questions", propositions=None, questions=None, author=None, tags=None, **kwargs):
        """Crée une manche Sel ou Poivre avec des questions."""
        if propositions is None:
            propositions = ["Noir", "Blanc"]
        if questions is None:
            questions = QuestionFactory.create_batch_sp(3, propositions=propositions)
        return cls.create(
            title=title,
            propositions=propositions,
            questions=questions,
            author=author,
            tags=tags,
            **kwargs,
        )


# ---------------------------------------------------------------------------
# MenuTheme (M2M through MenuThemeQuestion)
# ---------------------------------------------------------------------------


class MenuThemeFactory(DjangoModelFactory):
    class Meta:
        model = MenuTheme

    title = factory.Sequence(lambda n: f"Thème {n}")
    type = MENU_TYPE_CL
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags au thème de menu si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @factory.post_generation
    def question_ids(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            MenuThemeQuestion.objects.create(
                menu_theme=obj, question=q, order=order
            )

    @classmethod
    def create_classic(cls, title="Thème classique", question_ids=None, author=None, tags=None, **kwargs):
        inst = cls.create(title=title, type=MENU_TYPE_CL, author=author, tags=tags, **kwargs)
        if question_ids:
            for order, q in enumerate(question_ids):
                MenuThemeQuestion.objects.create(
                    menu_theme=inst, question=q, order=order
                )
        return inst

    @classmethod
    def create_troll(cls, title="Thème troll", question_ids=None, author=None, tags=None, **kwargs):
        inst = cls.create(title=title, type=MENU_TYPE_TR, author=author, tags=tags, **kwargs)
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
    author = None
    menu_1 = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_CL)
    menu_2 = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_CL)
    menu_troll = factory.SubFactory(MenuThemeFactory, type=MENU_TYPE_TR)

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags aux menus si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)


# ---------------------------------------------------------------------------
# Addition (M2M through AdditionQuestion)
# ---------------------------------------------------------------------------


class AdditionFactory(DjangoModelFactory):
    class Meta:
        model = Addition

    title = factory.Sequence(lambda n: f"Addition rapide {n}")
    original = False
    description = ""
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags à l'addition si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            AdditionQuestion.objects.create(
                addition=obj, question=q, order=order
            )

    @classmethod
    def create_with_questions(cls, title="Addition avec questions", questions=None, author=None, tags=None, **kwargs):
        """Crée une manche Addition avec des questions."""
        if questions is None:
            questions = QuestionFactory.create_batch_ad(3)
        return cls.create(title=title, questions=questions, author=author, tags=tags, **kwargs)


# ---------------------------------------------------------------------------
# DeadlyBurger (M2M through DeadlyBurgerQuestion)
# ---------------------------------------------------------------------------


class DeadlyBurgerFactory(DjangoModelFactory):
    class Meta:
        model = DeadlyBurger

    title = factory.Sequence(lambda n: f"Burger de la mort {n}")
    original = False
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags au burger de la mort si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @factory.post_generation
    def questions(obj, create, extracted, **kwargs):
        if not create or extracted is None:
            return
        for order, q in enumerate(extracted):
            DeadlyBurgerQuestion.objects.create(
                deadly_burger=obj, question=q, order=order
            )

    @classmethod
    def create_with_ten_questions(cls, title="Burger de la mort - Finale", author=None, tags=None, **kwargs):
        questions = [
            QuestionFactory.create_db(text=f"DB{i}") for i in range(1, 11)
        ]
        return cls.create(title=title, questions=questions, author=author, tags=tags, **kwargs)


# ---------------------------------------------------------------------------
# VideoInterlude
# ---------------------------------------------------------------------------


class VideoInterludeFactory(DjangoModelFactory):
    """Factory pour créer des interludes vidéo."""

    class Meta:
        model = VideoInterlude

    title = factory.Sequence(lambda n: f"Interlude {n}")
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    interlude_type = INTERLUDE_TYPE_IL
    duration_seconds = 30
    autoplay = True
    skip_allowed = True
    skip_after_seconds = None
    author = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags à l'interlude si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @classmethod
    def create_intro(cls, title="Intro", author=None, tags=None, **kwargs):
        """Crée un interlude de type Intro."""
        return cls.create(
            title=title,
            interlude_type=INTERLUDE_TYPE_IN,
            author=author,
            tags=tags,
            **kwargs,
        )

    @classmethod
    def create_outro(cls, title="Outro", author=None, tags=None, **kwargs):
        """Crée un interlude de type Outro."""
        return cls.create(
            title=title,
            interlude_type=INTERLUDE_TYPE_OU,
            author=author,
            tags=tags,
            **kwargs,
        )

    @classmethod
    def create_pub(cls, title="Pub", author=None, tags=None, **kwargs):
        """Crée un interlude de type Pub."""
        return cls.create(
            title=title,
            interlude_type=INTERLUDE_TYPE_PU,
            author=author,
            tags=tags,
            **kwargs,
        )


# ---------------------------------------------------------------------------
# BurgerQuiz (FKs optionnels)
# ---------------------------------------------------------------------------


class BurgerQuizFactory(DjangoModelFactory):
    class Meta:
        model = BurgerQuiz

    title = factory.Sequence(lambda n: f"Session test {n}")
    toss = "Consigne du toss."
    author = None
    nuggets = None
    salt_or_pepper = None
    menus = None
    addition = None
    deadly_burger = None

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Ajoute des tags au burger quiz si fournis."""
        if not create or extracted is None:
            return
        obj.tags.add(*extracted)

    @classmethod
    def create_full(cls, title="Session complète", toss="Toss complet", author=None, tags=None, **kwargs):
        """Burger Quiz avec toutes les manches créées automatiquement."""
        return cls.create(
            title=title,
            toss=toss,
            author=author,
            tags=tags,
            nuggets=NuggetsFactory.create(),
            salt_or_pepper=SaltOrPepperFactory.create(),
            menus=MenusFactory.create(),
            addition=AdditionFactory.create(),
            deadly_burger=DeadlyBurgerFactory.create(),
            **kwargs,
        )

    @classmethod
    def create_with_structure(
        cls,
        title="Session avec structure",
        toss="Toss",
        author=None,
        tags=None,
        interludes=None,
        **kwargs,
    ):
        """
        Burger Quiz avec toutes les manches et une structure personnalisée.
        
        Args:
            interludes: dict avec clés optionnelles 'intro', 'outro', 'pubs' (liste)
                       Si None, crée une structure par défaut sans interludes.
        """
        bq = cls.create_full(title=title, toss=toss, author=author, tags=tags, **kwargs)
        
        elements = []
        order = 1
        
        if interludes and interludes.get("intro"):
            elements.append(
                BurgerQuizElement(
                    burger_quiz=bq,
                    order=order,
                    element_type="interlude",
                    interlude=interludes["intro"],
                )
            )
            order += 1
        
        for round_type in [QUESTION_TYPE_NU, QUESTION_TYPE_SP, QUESTION_TYPE_ME, QUESTION_TYPE_AD, QUESTION_TYPE_DB]:
            elements.append(
                BurgerQuizElement(
                    burger_quiz=bq,
                    order=order,
                    element_type="round",
                    round_type=round_type,
                )
            )
            order += 1
            
            if interludes and interludes.get("pubs"):
                for pub in interludes["pubs"]:
                    if pub.get("after") == round_type:
                        elements.append(
                            BurgerQuizElement(
                                burger_quiz=bq,
                                order=order,
                                element_type="interlude",
                                interlude=pub["interlude"],
                            )
                        )
                        order += 1
        
        if interludes and interludes.get("outro"):
            elements.append(
                BurgerQuizElement(
                    burger_quiz=bq,
                    order=order,
                    element_type="interlude",
                    interlude=interludes["outro"],
                )
            )
        
        BurgerQuizElement.objects.bulk_create(elements)
        return bq


# ---------------------------------------------------------------------------
# BurgerQuizElement
# ---------------------------------------------------------------------------

class BurgerQuizElementFactory(DjangoModelFactory):
    """Factory pour créer des éléments de structure de Burger Quiz."""

    class Meta:
        model = BurgerQuizElement

    burger_quiz = factory.SubFactory(BurgerQuizFactory)
    order = factory.Sequence(lambda n: n + 1)
    element_type = "round"
    round_type = QUESTION_TYPE_NU
    interlude = None

    @classmethod
    def create_round(cls, burger_quiz, order, round_type):
        """Crée un élément de type manche."""
        return cls.create(
            burger_quiz=burger_quiz,
            order=order,
            element_type="round",
            round_type=round_type,
            interlude=None,
        )

    @classmethod
    def create_interlude(cls, burger_quiz, order, interlude):
        """Crée un élément de type interlude."""
        return cls.create(
            burger_quiz=burger_quiz,
            order=order,
            element_type="interlude",
            round_type=None,
            interlude=interlude,
        )
