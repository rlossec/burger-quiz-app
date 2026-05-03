# uv run manage.py test quiz.tests.questions.test_update
# PUT /api/quiz/questions/<id>/ — Mise à jour (mêmes contraintes que la création).


from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests import MANDATORY_FIELD_ERROR_MESSAGE
from ...tests import (
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
)
from ...tests.factories import QuestionFactory

User = get_user_model()


# ---------------------------------------------------------------------------
# Fixtures et helpers (alignés sur test_create)
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


def build_payload(question_type, text="Question", answers=None, **kwargs):
    if answers is None:
        answers = VALID_ANSWERS[question_type]
    return {
        "text": text,
        "question_type": question_type,
        "original": False,
        "answers": answers,
        **kwargs,
    }


# ---------------------------------------------------------------------------
# Base commune
# ---------------------------------------------------------------------------


class QuestionUpdateBaseTestCase(APITestCase):
    """Base pour les tests de mise à jour : URL détail, put, assertions."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="quiz_test_user",
            email="quiz_test@example.com",
            password="QuizTestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.question = QuestionFactory.create_nu_with_answers(text="Question à mettre à jour")
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    def put(self, payload):
        return self.client.put(self.url, payload, format="json")

    def assertOk(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assertBadRequest(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Contraintes communes (alignées sur test_create)
# ---------------------------------------------------------------------------


class TestQuestionUpdateValidation(QuestionUpdateBaseTestCase):
    """Mêmes règles de validation qu'à la création."""

    def test_missing_text_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(qtype, text="x")
                payload.pop("text")
                response = self.put(payload)
                self.assertBadRequest(response)
                self.assertEqual(response.data["text"], [MANDATORY_FIELD_ERROR_MESSAGE])

    def test_empty_text_returns_400(self):
        for text_value, label in [("", "vide"), ("   ", "espaces")]:
            with self.subTest(text=label):
                payload = build_payload(QUESTION_TYPE_NU, text=text_value)
                response = self.put(payload)
                self.assertBadRequest(response)
                self.assertIn("text", response.data)

    def test_missing_question_type_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(qtype)
                payload.pop("question_type")
                response = self.put(payload)
                self.assertBadRequest(response)
                self.assertEqual(
                    response.data["question_type"], [MANDATORY_FIELD_ERROR_MESSAGE]
                )

    def test_invalid_question_type_returns_400(self):
        payload = build_payload(QUESTION_TYPE_NU)
        payload["question_type"] = "XX"
        response = self.put(payload)
        self.assertBadRequest(response)

    def test_video_url_and_image_url_are_saved(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(
                    qtype,
                    text=f"Médias {label}",
                    video_url="https://example.com/video.mp4",
                    image_url="https://example.com/image.jpg",
                )
                response = self.put(payload)
                self.assertOk(response)
                self.question.refresh_from_db()
                self.assertEqual(self.question.video_url, payload["video_url"])
                self.assertEqual(self.question.image_url, payload["image_url"])

    def test_invalid_video_url_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(qtype, text=f"Question {label}")
                payload["video_url"] = "pas-une-url"
                response = self.put(payload)
                self.assertBadRequest(response)
                self.assertIn("video_url", response.data)

    def test_invalid_image_url_returns_400(self):
        for qtype, label in ALL_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(qtype, text=f"Question {label}")
                payload["image_url"] = "pas-une-url"
                response = self.put(payload)
                self.assertBadRequest(response)
                self.assertIn("image_url", response.data)

    def test_incorrect_answer_forbidden_for_open_types(self):
        trap_answers = [
            {"text": "Bonne réponse", "is_correct": True},
            {"text": "Piège", "is_correct": False},
        ]
        for qtype, label in OPEN_TYPES:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = build_payload(qtype, answers=trap_answers)
                self.assertBadRequest(self.put(payload))

    def test_missing_answers_returns_400_for_types_that_require_them(self):
        for qtype, label in TYPES_WITH_ANSWERS:
            with self.subTest(question_type=label):
                self._set_question_for_type(qtype)
                payload = {
                    "text": f"Sans answers {label}",
                    "question_type": qtype,
                    "original": False,
                }
                self.assertBadRequest(self.client.put(self.url, payload, format="json"))

    def _set_question_for_type(self, question_type):
        """Met à jour self.question et self.url pour le type donné."""
        if question_type == QUESTION_TYPE_NU:
            self.question = QuestionFactory.create_nu_with_answers()
        elif question_type == QUESTION_TYPE_SP:
            self.question = QuestionFactory.create_sp()
        elif question_type == QUESTION_TYPE_ME:
            self.question = QuestionFactory.create_me()
        elif question_type == QUESTION_TYPE_AD:
            self.question = QuestionFactory.create_ad()
        else:
            self.question = QuestionFactory.create_db()
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})


# ---------------------------------------------------------------------------
# Succès par type
# ---------------------------------------------------------------------------


class TestQuestionUpdateNU(QuestionUpdateBaseTestCase):

    def test_update_success(self):
        payload = build_payload(QUESTION_TYPE_NU, text="Nuggets mis à jour")
        response = self.put(payload)
        self.assertOk(response)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "Nuggets mis à jour")
        self.assertEqual(self.question.answers.count(), 4)
        self.assertEqual(self.question.answers.filter(is_correct=True).count(), 1)

    def test_wrong_number_of_answers_returns_400(self):
        payload = build_payload(
            QUESTION_TYPE_NU,
            answers=[{"text": "A", "is_correct": True}],
        )
        self.assertBadRequest(self.put(payload))

    def test_no_correct_answer_returns_400(self):
        payload = build_payload(
            QUESTION_TYPE_NU,
            answers=[{"text": f"R{i}", "is_correct": False} for i in range(4)],
        )
        self.assertBadRequest(self.put(payload))

    def test_multiple_correct_answers_returns_400(self):
        payload = build_payload(
            QUESTION_TYPE_NU,
            answers=[
                {"text": "A", "is_correct": True},
                {"text": "B", "is_correct": False},
                {"text": "C", "is_correct": True},
                {"text": "D", "is_correct": False},
            ],
        )
        self.assertBadRequest(self.put(payload))


class TestQuestionUpdateSP(QuestionUpdateBaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = QuestionFactory.create_sp()
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    def test_update_success(self):
        payload = build_payload(QUESTION_TYPE_SP, text="SP mis à jour")
        response = self.put(payload)
        self.assertOk(response)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "SP mis à jour")
        self.assertEqual(self.question.answers.filter(is_correct=True).count(), 2)


class TestQuestionUpdateME(QuestionUpdateBaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = QuestionFactory.create_me()
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    def test_update_success(self):
        payload = build_payload(QUESTION_TYPE_ME, text="ME mis à jour")
        response = self.put(payload)
        self.assertOk(response)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "ME mis à jour")
        self.assertEqual(self.question.answers.count(), 1)


class TestQuestionUpdateAD(QuestionUpdateBaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = QuestionFactory.create_ad()
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    def test_update_success(self):
        payload = build_payload(QUESTION_TYPE_AD, text="AD mis à jour")
        self.assertOk(self.put(payload))

    def test_all_incorrect_answers_returns_400(self):
        payload = build_payload(
            QUESTION_TYPE_AD,
            answers=[
                {"text": "A", "is_correct": False},
                {"text": "B", "is_correct": False},
            ],
        )
        self.assertBadRequest(self.put(payload))


class TestQuestionUpdateDB(QuestionUpdateBaseTestCase):

    def setUp(self):
        super().setUp()
        self.question = QuestionFactory.create_db()
        self.url = reverse("question-detail", kwargs={"pk": self.question.pk})

    def test_update_success_without_answers(self):
        payload = build_payload(QUESTION_TYPE_DB, text="DB mis à jour")
        response = self.put(payload)
        self.assertOk(response)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "DB mis à jour")
        self.assertEqual(self.question.answers.count(), 0)

    def test_update_with_answers_returns_400(self):
        payload = build_payload(
            QUESTION_TYPE_DB,
            answers=[{"text": "X", "is_correct": False}],
        )
        self.assertBadRequest(self.put(payload))
