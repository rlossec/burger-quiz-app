# python manage.py test quiz.tests.questions.test_create
# POST /api/quiz/questions/ — Création avec original, video_url, audio_url et réponses selon le type.

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import Question
from ...tests import (
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
)


def _nu_answers(one_correct_index=2):
    """4 réponses NU : une seule is_correct à l'index donné."""
    return [
        {"text": c, "is_correct": i == one_correct_index}
        for i, c in enumerate(["A", "B", "C", "D"])
    ]


class TestQuestionCreateEndpoint(APITestCase):
    """POST /api/quiz/questions/ — Création avec original, video_url, audio_url et réponses selon le type."""

    def setUp(self):
        self.url = reverse("question-list")
        self.valid_nuggets_payload = {
            "text": "Nouvelle question Nuggets",
            "question_type": QUESTION_TYPE_NU,
            "original": False,
            "answers": _nu_answers(one_correct_index=2),
        }

    def test_create_nuggets_success(self):
        """NU : exactement 4 réponses, une et une seule is_correct (spéc §5.2)."""
        response = self.client.post(self.url, self.valid_nuggets_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["text"], self.valid_nuggets_payload["text"])
        self.assertEqual(response.data["question_type"], QUESTION_TYPE_NU)
        self.assertEqual(response.data["original"], False)
        self.assertEqual(
            Question.objects.filter(text=self.valid_nuggets_payload["text"]).count(), 1
        )
        q = Question.objects.get(text=self.valid_nuggets_payload["text"])
        self.assertEqual(q.answers.count(), 4)
        self.assertEqual(q.answers.filter(is_correct=True).count(), 1)

    def test_create_accepts_video_url_audio_url(self):
        payload = {
            **self.valid_nuggets_payload,
            "video_url": "https://example.com/video.mp4",
            "audio_url": "https://example.com/audio.mp3",
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        q = Question.objects.get(text=payload["text"])
        self.assertEqual(q.video_url, payload["video_url"])
        self.assertEqual(q.image_url, payload["audio_url"])

    def test_create_missing_text_returns_400(self):
        payload = self.valid_nuggets_payload.copy()
        payload.pop("text")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("text", response.data)

    def test_create_missing_question_type_returns_400(self):
        payload = self.valid_nuggets_payload.copy()
        payload.pop("question_type")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("question_type", response.data)

    # ——— NU : 4 réponses, une seule is_correct ———
    def test_create_nuggets_not_four_answers_returns_400(self):
        """NU : exactement 4 réponses requises."""
        for num_answers, answers in [
            (1, [{"text": "A", "is_correct": True}]),
            (5, _nu_answers() + [{"text": "E", "is_correct": False}]),
        ]:
            payload = {
                "text": f"NU pas 4 réponses ({num_answers})",
                "question_type": QUESTION_TYPE_NU,
                "original": False,
                "answers": answers,
            }
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                msg=f"NU avec {len(answers)} réponses doit retourner 400",
            )

    def test_create_nuggets_no_correct_answer_returns_400(self):
        """NU : au moins une réponse is_correct=true requise."""
        payload = {
            "text": "NU sans bonne réponse",
            "question_type": QUESTION_TYPE_NU,
            "original": False,
            "answers": [{"text": f"R{i}", "is_correct": False} for i in range(4)],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_nuggets_multiple_correct_returns_400(self):
        """NU : une seule réponse is_correct=true autorisée."""
        payload = {
            "text": "NU deux bonnes réponses",
            "question_type": QUESTION_TYPE_NU,
            "original": False,
            "answers": [
                {"text": "A", "is_correct": True},
                {"text": "B", "is_correct": False},
                {"text": "C", "is_correct": True},
                {"text": "D", "is_correct": False},
            ],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ——— SP : plusieurs réponses exactes possibles, pas de leurres ———
    def test_create_sp_success(self):
        """SP : plusieurs is_correct=true autorisés."""
        payload = {
            "text": "Question Sel ou poivre",
            "question_type": QUESTION_TYPE_SP,
            "original": False,
            "answers": [
                {"text": "Réponse 1", "is_correct": True},
                {"text": "Réponse 2", "is_correct": True},
                {"text": "Réponse 3", "is_correct": False},
            ],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        q = Question.objects.get(text=payload["text"])
        self.assertEqual(q.answers.filter(is_correct=True).count(), 2)

    # ——— ME : une réponse exacte, pas de leurres ———
    def test_create_me_success(self):
        """ME : une réponse is_correct=true."""
        payload = {
            "text": "Question Menu",
            "question_type": QUESTION_TYPE_ME,
            "original": False,
            "answers": [{"text": "La bonne réponse", "is_correct": True}],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        q = Question.objects.get(text=payload["text"])
        self.assertEqual(q.answers.count(), 1)
        self.assertTrue(q.answers.first().is_correct)

    # ——— AD : une réponse exacte ou pas de réponse possible ———
    def test_create_ad_success(self):
        """AD : une réponse correcte."""
        payload = {
            "text": "Question Addition",
            "question_type": QUESTION_TYPE_AD,
            "original": False,
            "answers": [{"text": "42", "is_correct": True}],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_ad_all_incorrect_returns_400(self):
        """AD : si answers fournies, au moins une is_correct=true requise."""
        payload = {
            "text": "AD sans bonne réponse",
            "question_type": QUESTION_TYPE_AD,
            "original": False,
            "answers": [
                {"text": "A", "is_correct": False},
                {"text": "B", "is_correct": False},
            ],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ——— DB : pas de réponses ———
    def test_create_db_success_empty_answers(self):
        """DB : pas de réponses ; answers absentes ou vides acceptées."""
        payload = {
            "text": "Question Burger de la mort",
            "question_type": QUESTION_TYPE_DB,
            "original": False,
            "answers": [],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        q = Question.objects.get(text=payload["text"])
        self.assertEqual(q.answers.count(), 0)

    def test_create_db_with_answers_returns_400(self):
        """DB : ne doit pas accepter de réponses."""
        payload = {
            "text": "DB avec réponses",
            "question_type": QUESTION_TYPE_DB,
            "original": False,
            "answers": [{"text": "X", "is_correct": False}],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ——— Général : answers requis pour NU, SP, ME, AD ———
    def test_create_requires_answers_for_nu_sp_me_ad(self):
        """Sans answers : 400 pour NU, SP, ME, AD."""
        for qtype, label in [
            (QUESTION_TYPE_NU, "NU"),
            (QUESTION_TYPE_SP, "SP"),
            (QUESTION_TYPE_ME, "ME"),
            (QUESTION_TYPE_AD, "AD"),
        ]:
            payload = {
                "text": f"Question sans answers {label}",
                "question_type": qtype,
                "original": False,
            }
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                msg=f"{label} sans answers doit retourner 400",
            )

    def test_create_invalid_question_type_returns_400(self):
        """question_type invalide → 400."""
        payload = {
            "text": "Question type invalide",
            "question_type": "XX",
            "original": False,
            "answers": [],
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
