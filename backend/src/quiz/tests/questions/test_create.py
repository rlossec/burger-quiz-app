# uv run manage.py test quiz.tests.questions.test_create
# POST /api/quiz/questions/ — Création avec original, video_url, image_url et réponses selon le type.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Question
from ...tests import MANDATORY_FIELD_ERROR_MESSAGE
from ...tests import (
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
)

# ---------------------------------------------------------------------------
# Fixtures et helpers
# ---------------------------------------------------------------------------

VALID_ANSWERS = {
    QUESTION_TYPE_NU: [
        {"text": c, "is_correct": i == 2}
        for i, c in enumerate(["A", "B", "C", "D"])
    ],
    QUESTION_TYPE_SP: [
        {"text": "R1", "is_correct": True},
        {"text": "R2", "is_correct": True},
    ],
    QUESTION_TYPE_ME: [{"text": "Réponse", "is_correct": True}],
    QUESTION_TYPE_AD: [{"text": "42", "is_correct": True}],
    QUESTION_TYPE_DB: [],
}

ALL_TYPES = [
    (QUESTION_TYPE_NU, "NU"),
    (QUESTION_TYPE_SP, "SP"),
    (QUESTION_TYPE_ME, "ME"),
    (QUESTION_TYPE_AD, "AD"),
    (QUESTION_TYPE_DB, "DB"),
]

OPEN_TYPES = [
    (QUESTION_TYPE_SP, "SP"),
    (QUESTION_TYPE_ME, "ME"),
    (QUESTION_TYPE_AD, "AD"),
]

TYPES_WITH_ANSWERS = [
    (QUESTION_TYPE_NU, "NU"),
    (QUESTION_TYPE_SP, "SP"),
    (QUESTION_TYPE_ME, "ME"),
    (QUESTION_TYPE_AD, "AD"),
]


# ---------------------------------------------------------------------------
# Base commune à tous les tests
# ---------------------------------------------------------------------------

class QuestionCreateBaseTestCase(APITestCase):
    """
    Classe de base : accès à l'URL, builder de payload, et helper de création.
    Toutes les classes de test en héritent.
    """

    def setUp(self):
        self.url = reverse("question-list")

    def build_payload(self, question_type, text="Question", answers=None, **kwargs):
        """
        Construit un payload valide pour le type donné.
        Si answers est None, utilise VALID_ANSWERS[question_type].
        """
        if answers is None:
            answers = VALID_ANSWERS[question_type]
        return {
            "text": text,
            "question_type": question_type,
            "original": False,
            "answers": answers,
            **kwargs,
        }

    def post(self, payload):
        return self.client.post(self.url, payload, format="json")

    def assertCreated(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def assertBadRequest(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------------
# Contraintes communes à tous les types
# ---------------------------------------------------------------------------

class TestQuestionCreateValidation(QuestionCreateBaseTestCase):
    """Champs obligatoires et contraintes valables pour tous les types."""

    def test_missing_text_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(qtype, text="x")
                payload.pop("text")
                response = self.post(payload)
                self.assertBadRequest(response)
                self.assertEqual(response.data["text"], [MANDATORY_FIELD_ERROR_MESSAGE])

    def test_empty_text_returns_400(self):
        """La question ne doit pas être vide (chaîne vide ou uniquement des espaces)."""
        for text_value, label in [("", "vide"), ("   ", "espaces")]:
            with self.subTest(text=label):
                payload = self.build_payload(QUESTION_TYPE_NU, text=text_value)
                response = self.post(payload)
                self.assertBadRequest(response)
                self.assertIn("text", response.data)

    def test_missing_question_type_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(qtype)
                payload.pop("question_type")
                response = self.post(payload)
                self.assertBadRequest(response)
                self.assertEqual(
                    response.data["question_type"], [MANDATORY_FIELD_ERROR_MESSAGE]
                )

    def test_invalid_question_type_returns_400(self):
        payload = self.build_payload(QUESTION_TYPE_NU)
        payload["question_type"] = "XX"
        response = self.post(payload)
        self.assertBadRequest(response)

    def test_video_url_and_image_url_are_saved(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(
                    qtype,
                    text=f"Médias {label}",  # texte unique par subTest
                    video_url="https://example.com/video.mp4",
                    image_url="https://example.com/image.jpg",
                )
                response = self.post(payload)
                self.assertCreated(response)
                q = Question.objects.get(pk=response.data["id"])  # pk, pas text
                self.assertEqual(q.video_url, payload["video_url"])
                self.assertEqual(q.image_url, payload["image_url"])

    def test_invalid_video_url_returns_400(self):
        """video_url doit être une URL valide."""
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(qtype, text=f"Question {label}")
                payload["video_url"] = "pas-une-url"
                response = self.post(payload)
                self.assertBadRequest(response)
                self.assertIn("video_url", response.data)

    def test_invalid_image_url_returns_400(self):
        """image_url doit être une URL valide."""
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(qtype, text=f"Question {label}")
                payload["image_url"] = "pas-une-url"
                response = self.post(payload)
                self.assertBadRequest(response)
                self.assertIn("image_url", response.data)

    def test_incorrect_answer_forbidden_for_open_types(self):
        """SP, ME, AD n'acceptent pas de réponse is_correct=False (pas de pièges)."""
        trap_answers = [
            {"text": "Bonne réponse", "is_correct": True},
            {"text": "Piège", "is_correct": False},
        ]
        for qtype, label in OPEN_TYPES:
            with self.subTest(question_type=label):
                payload = self.build_payload(qtype, answers=trap_answers)
                self.assertBadRequest(self.post(payload))

    def test_missing_answers_returns_400_for_types_that_require_them(self):
        """NU, SP, ME, AD : answers obligatoire."""
        for qtype, label in TYPES_WITH_ANSWERS:
            with self.subTest(question_type=label):
                payload = {
                    "text": f"Sans answers {label}",
                    "question_type": qtype,
                    "original": False,
                }
                self.assertBadRequest(self.post(payload))

# ---------------------------------------------------------------------------
# NU — Nuggets
# ---------------------------------------------------------------------------

class TestQuestionCreateNU(QuestionCreateBaseTestCase):

    def test_create_success(self):
        payload = self.build_payload(QUESTION_TYPE_NU, text="Nuggets valide")
        response = self.post(payload)
        self.assertCreated(response)
        q = Question.objects.get(pk=response.data["id"])
        self.assertEqual(q.answers.count(), 4)
        self.assertEqual(q.answers.filter(is_correct=True).count(), 1)

    def test_wrong_number_of_answers_returns_400(self):
        for answers, label in [
            ([{"text": "A", "is_correct": True}], "1 réponse"),
            (VALID_ANSWERS[QUESTION_TYPE_NU] + [{"text": "E", "is_correct": False}], "5 réponses"),
        ]:
            with self.subTest(cas=label):
                payload = self.build_payload(QUESTION_TYPE_NU, answers=answers)
                self.assertBadRequest(self.post(payload))

    def test_no_correct_answer_returns_400(self):
        answers = [{"text": f"R{i}", "is_correct": False} for i in range(4)]
        payload = self.build_payload(QUESTION_TYPE_NU, answers=answers)
        self.assertBadRequest(self.post(payload))

    def test_multiple_correct_answers_returns_400(self):
        answers = [
            {"text": "A", "is_correct": True},
            {"text": "B", "is_correct": False},
            {"text": "C", "is_correct": True},
            {"text": "D", "is_correct": False},
        ]
        payload = self.build_payload(QUESTION_TYPE_NU, answers=answers)
        self.assertBadRequest(self.post(payload))


# ---------------------------------------------------------------------------
# SP — Sel ou poivre
# ---------------------------------------------------------------------------

class TestQuestionCreateSP(QuestionCreateBaseTestCase):

    def test_create_success(self):
        payload = self.build_payload(QUESTION_TYPE_SP, text="SP valide")
        response = self.post(payload)
        self.assertCreated(response)
        q = Question.objects.get(pk=response.data["id"])
        self.assertEqual(q.answers.filter(is_correct=True).count(), 2)


# ---------------------------------------------------------------------------
# ME — Menu
# ---------------------------------------------------------------------------

class TestQuestionCreateME(QuestionCreateBaseTestCase):

    def test_create_success(self):
        payload = self.build_payload(QUESTION_TYPE_ME, text="ME valide")
        response = self.post(payload)
        self.assertCreated(response)
        q = Question.objects.get(pk=response.data["id"])
        self.assertEqual(q.answers.count(), 1)
        self.assertTrue(q.answers.first().is_correct)


# ---------------------------------------------------------------------------
# AD — Addition
# ---------------------------------------------------------------------------

class TestQuestionCreateAD(QuestionCreateBaseTestCase):

    def test_create_success(self):
        payload = self.build_payload(QUESTION_TYPE_AD, text="AD valide")
        self.assertCreated(self.post(payload))

    def test_all_incorrect_answers_returns_400(self):
        answers = [{"text": "A", "is_correct": False}, {"text": "B", "is_correct": False}]
        payload = self.build_payload(QUESTION_TYPE_AD, answers=answers)
        self.assertBadRequest(self.post(payload))


# ---------------------------------------------------------------------------
# DB — Burger de la mort
# ---------------------------------------------------------------------------

class TestQuestionCreateDB(QuestionCreateBaseTestCase):

    def test_create_success_without_answers(self):
        payload = self.build_payload(QUESTION_TYPE_DB, text="DB valide")
        response = self.post(payload)
        self.assertCreated(response)
        q = Question.objects.get(pk=response.data["id"])
        self.assertEqual(q.answers.count(), 0)

    def test_create_with_answers_returns_400(self):
        answers = [{"text": "X", "is_correct": False}]
        payload = self.build_payload(QUESTION_TYPE_DB, answers=answers)
        self.assertBadRequest(self.post(payload))