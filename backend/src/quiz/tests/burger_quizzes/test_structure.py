# python manage.py test quiz.tests.burger_quizzes.test_structure
# GET/PUT /api/quiz/burger-quizzes/{id}/structure/ — Structure du Burger Quiz.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import BurgerQuizElement
from ..factories import (
    BurgerQuizFactory,
    VideoInterludeFactory,
    BurgerQuizElementFactory,
)
from .. import (
    QUESTION_TYPE_NU,
    QUESTION_TYPE_SP,
    QUESTION_TYPE_ME,
    QUESTION_TYPE_AD,
    QUESTION_TYPE_DB,
    STRUCTURE_DUPLICATE_ROUND_TYPE,
    STRUCTURE_ROUND_NOT_ATTACHED,
    STRUCTURE_INTERLUDE_NOT_FOUND,
)

User = get_user_model()


class TestBurgerQuizStructureReadEndpoint(APITestCase):
    """GET /api/quiz/burger-quizzes/{id}/structure/ — Lecture de la structure."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.bq = BurgerQuizFactory.create_full(title="Quiz complet")
        self.url = reverse("burger-quiz-structure", kwargs={"pk": self.bq.pk})

    def test_get_structure_empty(self):
        """Structure vide si non configurée (retourne structure par défaut)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["burger_quiz_id"], str(self.bq.id))
        self.assertIn("elements", response.data)

    def test_get_structure_with_elements(self):
        """Structure avec éléments configurés."""
        intro = VideoInterludeFactory.create_intro(title="Intro")
        outro = VideoInterludeFactory.create_outro(title="Outro")
        
        BurgerQuizElementFactory.create_interlude(self.bq, order=1, interlude=intro)
        BurgerQuizElementFactory.create_round(self.bq, order=2, round_type=QUESTION_TYPE_NU)
        BurgerQuizElementFactory.create_round(self.bq, order=3, round_type=QUESTION_TYPE_SP)
        BurgerQuizElementFactory.create_round(self.bq, order=4, round_type=QUESTION_TYPE_ME)
        BurgerQuizElementFactory.create_round(self.bq, order=5, round_type=QUESTION_TYPE_AD)
        BurgerQuizElementFactory.create_round(self.bq, order=6, round_type=QUESTION_TYPE_DB)
        BurgerQuizElementFactory.create_interlude(self.bq, order=7, interlude=outro)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 7)
        
        self.assertEqual(response.data["elements"][0]["element_type"], "interlude")
        self.assertEqual(response.data["elements"][0]["order"], 1)
        
        self.assertEqual(response.data["elements"][1]["element_type"], "round")
        self.assertEqual(response.data["elements"][1]["round_type"], QUESTION_TYPE_NU)

    def test_get_structure_not_found(self):
        """404 si le Burger Quiz n'existe pas."""
        url = reverse("burger-quiz-structure", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_structure_elements_ordered(self):
        """Les éléments sont retournés dans l'ordre."""
        BurgerQuizElementFactory.create_round(self.bq, order=3, round_type=QUESTION_TYPE_ME)
        BurgerQuizElementFactory.create_round(self.bq, order=1, round_type=QUESTION_TYPE_NU)
        BurgerQuizElementFactory.create_round(self.bq, order=2, round_type=QUESTION_TYPE_SP)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        orders = [el["order"] for el in response.data["elements"]]
        self.assertEqual(orders, [1, 2, 3])


class TestBurgerQuizStructureUpdateEndpoint(APITestCase):
    """PUT /api/quiz/burger-quizzes/{id}/structure/ — Mise à jour de la structure."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.bq = BurgerQuizFactory.create_full(title="Quiz complet")
        self.intro = VideoInterludeFactory.create_intro(title="Intro")
        self.outro = VideoInterludeFactory.create_outro(title="Outro")
        self.pub = VideoInterludeFactory.create_pub(title="Pub")
        self.url = reverse("burger-quiz-structure", kwargs={"pk": self.bq.pk})

    def test_put_structure_success(self):
        """Remplacement complet de la structure."""
        payload = {
            "elements": [
                {"element_type": "interlude", "interlude_id": str(self.intro.id)},
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
                {"element_type": "round", "round_type": QUESTION_TYPE_SP},
                {"element_type": "interlude", "interlude_id": str(self.pub.id)},
                {"element_type": "round", "round_type": QUESTION_TYPE_ME},
                {"element_type": "round", "round_type": QUESTION_TYPE_AD},
                {"element_type": "round", "round_type": QUESTION_TYPE_DB},
                {"element_type": "interlude", "interlude_id": str(self.outro.id)},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 8)
        
        elements = BurgerQuizElement.objects.filter(burger_quiz=self.bq).order_by("order")
        self.assertEqual(elements.count(), 8)
        self.assertEqual(elements[0].element_type, "interlude")
        self.assertEqual(elements[0].interlude, self.intro)
        self.assertEqual(elements[1].element_type, "round")
        self.assertEqual(elements[1].round_type, QUESTION_TYPE_NU)

    def test_put_structure_replaces_existing(self):
        """PUT remplace entièrement la structure existante."""
        BurgerQuizElementFactory.create_round(self.bq, order=1, round_type=QUESTION_TYPE_NU)
        BurgerQuizElementFactory.create_round(self.bq, order=2, round_type=QUESTION_TYPE_SP)
        
        self.assertEqual(BurgerQuizElement.objects.filter(burger_quiz=self.bq).count(), 2)
        
        payload = {
            "elements": [
                {"element_type": "round", "round_type": QUESTION_TYPE_ME},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        elements = BurgerQuizElement.objects.filter(burger_quiz=self.bq)
        self.assertEqual(elements.count(), 1)
        self.assertEqual(elements[0].round_type, QUESTION_TYPE_ME)

    def test_put_structure_order_from_position(self):
        """L'ordre est déterminé par la position dans le tableau."""
        payload = {
            "elements": [
                {"element_type": "round", "round_type": QUESTION_TYPE_DB},
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
                {"element_type": "round", "round_type": QUESTION_TYPE_ME},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data["elements"][0]["order"], 1)
        self.assertEqual(response.data["elements"][0]["round_type"], QUESTION_TYPE_DB)
        self.assertEqual(response.data["elements"][1]["order"], 2)
        self.assertEqual(response.data["elements"][1]["round_type"], QUESTION_TYPE_NU)
        self.assertEqual(response.data["elements"][2]["order"], 3)
        self.assertEqual(response.data["elements"][2]["round_type"], QUESTION_TYPE_ME)

    def test_put_structure_duplicate_round_type_error(self):
        """Erreur si un type de manche apparaît plusieurs fois."""
        payload = {
            "elements": [
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_round_not_attached_error(self):
        """Erreur si une manche référencée n'est pas attachée au Burger Quiz."""
        bq_without_nuggets = BurgerQuizFactory.create(
            title="Quiz sans nuggets",
            nuggets=None,
        )
        url = reverse("burger-quiz-structure", kwargs={"pk": bq_without_nuggets.pk})
        
        payload = {
            "elements": [
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
            ]
        }
        
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_interlude_not_found_error(self):
        """Erreur si un interlude référencé n'existe pas."""
        payload = {
            "elements": [
                {"element_type": "interlude", "interlude_id": str(uuid.uuid4())},
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_not_found(self):
        """404 si le Burger Quiz n'existe pas."""
        url = reverse("burger-quiz-structure", kwargs={"pk": uuid.uuid4()})
        payload = {"elements": []}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_structure_empty_elements(self):
        """Structure vide est valide."""
        payload = {"elements": []}
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["elements"], [])

    def test_put_structure_multiple_interludes_allowed(self):
        """Plusieurs interludes du même type sont autorisés."""
        pub2 = VideoInterludeFactory.create_pub(title="Pub 2")
        
        payload = {
            "elements": [
                {"element_type": "interlude", "interlude_id": str(self.pub.id)},
                {"element_type": "round", "round_type": QUESTION_TYPE_NU},
                {"element_type": "interlude", "interlude_id": str(pub2.id)},
                {"element_type": "round", "round_type": QUESTION_TYPE_SP},
                {"element_type": "interlude", "interlude_id": str(self.pub.id)},
            ]
        }
        
        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 5)
