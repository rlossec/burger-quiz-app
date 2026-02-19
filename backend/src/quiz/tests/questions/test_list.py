
from unittest import skip

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...tests import (
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
)
from ...tests.factories import QuestionFactory


# Catégories de questions pour le test paramétré (code API → attribut de la question en setUp)
QUESTION_TYPE_CATEGORIES = [
    ("NU", "q_nu", "Nuggets"),
    ("SP", "q_sp", "Sel ou poivre"),
    ("ME", "q_me", "Menu"),
    ("AD", "q_ad", "Addition"),
    ("DB", "q_db", "Burger de la mort"),
]




class TestQuestionListEndpoint(APITestCase):
    """
    Test de l'endpoint GET /api/quiz/questions/
    Commande : uv run manage.py test quiz.tests.questions.test_list
    """

    def setUp(self):
        self.url = reverse("question-list")
        self.q_nu = QuestionFactory.create_nu("Question Nuggets", original=False)
        self.q_sp = QuestionFactory.create_sp("Question SP", original=True)
        self.q_me = QuestionFactory.create_me("Question ME", original=False)
        self.q_ad = QuestionFactory.create_ad("Question AD", original=True)
        self.q_db = QuestionFactory.create_db("Question DB", original=False)
        self.questions_by_type = {
            QUESTION_TYPE_NU: self.q_nu,
            QUESTION_TYPE_SP: self.q_sp,
            QUESTION_TYPE_ME: self.q_me,
            QUESTION_TYPE_AD: self.q_ad,
            QUESTION_TYPE_DB: self.q_db,
        }
        self.all_question_ids = {str(q.id) for q in self.questions_by_type.values()}

    # 1. Cas simple de succès : GET /api/quiz/questions/ 
    def test_list_questions_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results", response.data)), 5)
        for question in response.data.get("results", response.data):
            self.assertIn("id", question)
            self.assertIn("text", question)
            self.assertIn("question_type", question)
            self.assertIn("original", question)
            self.assertIn("usage_count", question)
            self.assertIn("created_at", question)
            self.assertIn("updated_at", question)

    # 2. Champ calculé usage_count : GET /api/quiz/questions/ 
    @skip("Not implemented")
    def test_list_exposes_usage_count(self):
        """Champ calculé usage_count."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get("results", response.data)
        if data:
            self.assertIn("usage_count", data[0])

    # 3. Filtre question_type : GET /api/quiz/questions/?question_type=<type>
    def test_list_questions_success_with_filter_question_type_per_category(self):
        """Test paramétré : pour chaque type (NU, SP, ME, AD, DB), le filtre question_type ne renvoie que les questions de ce type."""
        for question_type, attr, label in QUESTION_TYPE_CATEGORIES:
            with self.subTest(question_type=question_type, category=label):
                response = self.client.get(self.url, {"question_type": question_type})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                ids = [item["id"] for item in response.data.get("results", response.data)]
                expected_question = getattr(self, attr)
                self.assertIn(str(expected_question.id), ids)
                # Les autres types ne doivent pas apparaître
                other_ids = self.all_question_ids - {str(expected_question.id)}
                for other_id in other_ids:
                    self.assertNotIn(other_id, ids, msg=f"question_type={question_type} ne doit pas contenir {other_id}")

    # 4. Filtre original : GET /api/quiz/questions/?original=true|false
    def test_list_filter_original(self):
        """Deux sous-tests : original=true (seulement q_sp, q_ad) et original=false (q_nu, q_me, q_db)."""
        original_true_ids = {str(self.q_sp.id), str(self.q_ad.id)}
        original_false_ids = {str(self.q_nu.id), str(self.q_me.id), str(self.q_db.id)}
        for original_param, expected_ids, excluded_ids in [
            ("true", original_true_ids, original_false_ids),
            ("false", original_false_ids, original_true_ids),
        ]:
            with self.subTest(original=original_param):
                response = self.client.get(self.url, {"original": original_param})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                ids = [item["id"] for item in response.data.get("results", response.data)]
                for eid in expected_ids:
                    self.assertIn(eid, ids, msg=f"original={original_param} doit contenir {eid}")
                for oid in excluded_ids:
                    self.assertNotIn(oid, ids, msg=f"original={original_param} ne doit pas contenir {oid}")
