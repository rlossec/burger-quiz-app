# python manage.py test quiz.tests.burger_quizzes.test_structure
# GET/PUT /api/quiz/burger-quizzes/{id}/structure/ — Structure du Burger Quiz.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import BurgerQuizElement
from ...serializers.structure import STRUCTURE_TYPE_TO_MODEL
from ..factories import (
    AdditionFactory,
    BurgerQuizFactory,
    DeadlyBurgerFactory,
    MenusFactory,
    NuggetsFactory,
    SaltOrPepperFactory,
    VideoInterludeFactory,
    BurgerQuizElementFactory,
)
User = get_user_model()


def _element_id_for_slug(bq, slug: str) -> str:
    model = STRUCTURE_TYPE_TO_MODEL[slug]
    for row in bq.structure_elements.select_related(
        "round",
        "interlude",
        "round__nuggets",
        "round__salt_or_pepper",
        "round__menus",
        "round__addition",
        "round__deadly_burger",
    ).order_by("order"):
        c = row.content
        if c is not None and isinstance(c, model):
            return str(c.id)
    raise AssertionError(f"Aucun élément de structure pour le slug {slug!r}")


def _payload_full_order(bq, intro, pub, outro):
    """Ordre : intro, NU, SP, pub, ME, AD, DB, outro."""
    return {
        "elements": [
            {"type": "video_interlude", "id": str(intro.id)},
            {"type": "nuggets", "id": _element_id_for_slug(bq, "nuggets")},
            {"type": "salt_or_pepper", "id": _element_id_for_slug(bq, "salt_or_pepper")},
            {"type": "video_interlude", "id": str(pub.id)},
            {"type": "menus", "id": _element_id_for_slug(bq, "menus")},
            {"type": "addition", "id": _element_id_for_slug(bq, "addition")},
            {"type": "deadly_burger", "id": _element_id_for_slug(bq, "deadly_burger")},
            {"type": "video_interlude", "id": str(outro.id)},
        ]
    }


class TestBurgerQuizStructureAuth(APITestCase):
    """GET/PUT structure — authentification requise (REST_FRAMEWORK default)."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.bq = BurgerQuizFactory.create_full(title="Quiz complet")
        self.url = reverse("burger-quiz-structure", kwargs={"pk": self.bq.pk})

    def test_get_structure_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_structure_requires_authentication(self):
        response = self.client.put(self.url, {"elements": []}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_get_structure_default_order(self):
        """create_full : 5 BurgerQuizElement dans l'ordre NU → SP → ME → AD → DB."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["burger_quiz_id"], str(self.bq.id))
        elements = response.data["elements"]
        self.assertEqual(len(elements), 5)
        types = [e["type"] for e in elements]
        self.assertEqual(
            types,
            ["nuggets", "salt_or_pepper", "menus", "addition", "deadly_burger"],
        )
        self.assertEqual(elements[0]["id"], _element_id_for_slug(self.bq, "nuggets"))

    def test_get_structure_with_custom_rows(self):
        """Ordre persisté (lignes BurgerQuizElement)."""
        intro = VideoInterludeFactory.create_intro(title="Intro")
        outro = VideoInterludeFactory.create_outro(title="Outro")

        BurgerQuizElement.objects.filter(burger_quiz=self.bq).delete()

        BurgerQuizElementFactory.create_interlude(self.bq, order=1, interlude=intro)
        BurgerQuizElementFactory.create_round(self.bq, order=2, round_obj=NuggetsFactory.create())
        BurgerQuizElementFactory.create_round(self.bq, order=3, round_obj=SaltOrPepperFactory.create())
        BurgerQuizElementFactory.create_round(self.bq, order=4, round_obj=MenusFactory.create())
        BurgerQuizElementFactory.create_round(self.bq, order=5, round_obj=AdditionFactory.create())
        BurgerQuizElementFactory.create_round(self.bq, order=6, round_obj=DeadlyBurgerFactory.create())
        BurgerQuizElementFactory.create_interlude(self.bq, order=7, interlude=outro)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 7)

        self.assertEqual(response.data["elements"][0]["type"], "video_interlude")
        self.assertEqual(response.data["elements"][0]["order"], 1)

        self.assertEqual(response.data["elements"][1]["type"], "nuggets")
        self.assertEqual(response.data["elements"][1]["order"], 2)

    def test_get_structure_not_found(self):
        """404 si le Burger Quiz n'existe pas."""
        url = reverse("burger-quiz-structure", kwargs={"pk": uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_structure_elements_ordered(self):
        """Les éléments sont retournés dans l'ordre persisté."""
        bq = BurgerQuizFactory.create(title="Quiz partiel")
        me = MenusFactory.create()
        n = NuggetsFactory.create()
        sp = SaltOrPepperFactory.create()
        BurgerQuizElementFactory.create_round(bq, order=3, round_obj=me)
        BurgerQuizElementFactory.create_round(bq, order=1, round_obj=n)
        BurgerQuizElementFactory.create_round(bq, order=2, round_obj=sp)

        url = reverse("burger-quiz-structure", kwargs={"pk": bq.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        orders = [el["order"] for el in response.data["elements"]]
        self.assertEqual(orders, [1, 2, 3])

    def test_get_structure_elements_include_nested_payload(self):
        """Réponse GET : chaque élément contient order, type, id et l'objet imbriqué sous la clé du type."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first = response.data["elements"][0]
        self.assertIn("order", first)
        self.assertIn("type", first)
        self.assertIn("id", first)
        self.assertEqual(first["type"], "nuggets")
        self.assertIn("nuggets", first)
        self.assertEqual(first["nuggets"]["id"], first["id"])


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
        """Remplacement complet de la structure (ordre = position dans le tableau)."""
        payload = _payload_full_order(self.bq, self.intro, self.pub, self.outro)

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 8)

        elements = BurgerQuizElement.objects.filter(burger_quiz=self.bq).order_by("order")
        self.assertEqual(elements.count(), 8)

    def test_put_structure_replaces_existing(self):
        """PUT remplace entièrement la structure existante."""
        BurgerQuizElement.objects.filter(burger_quiz=self.bq).delete()
        n = NuggetsFactory.create()
        sp = SaltOrPepperFactory.create()
        BurgerQuizElementFactory.create_round(self.bq, order=1, round_obj=n)
        BurgerQuizElementFactory.create_round(self.bq, order=2, round_obj=sp)

        self.assertEqual(BurgerQuizElement.objects.filter(burger_quiz=self.bq).count(), 2)

        menus = MenusFactory.create()
        payload = {
            "elements": [
                {"type": "menus", "id": str(menus.id)},
            ]
        }

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        elements = BurgerQuizElement.objects.filter(burger_quiz=self.bq)
        self.assertEqual(elements.count(), 1)
        self.assertEqual(elements[0].content, menus)

    def test_put_structure_order_from_array_position(self):
        """L'ordre d'apparition suit la position dans le tableau (order 1, 2, 3…)."""
        payload = {
            "elements": [
                {"type": "deadly_burger", "id": _element_id_for_slug(self.bq, "deadly_burger")},
                {"type": "nuggets", "id": _element_id_for_slug(self.bq, "nuggets")},
                {"type": "menus", "id": _element_id_for_slug(self.bq, "menus")},
            ]
        }

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["elements"][0]["order"], 1)
        self.assertEqual(response.data["elements"][0]["type"], "deadly_burger")
        self.assertEqual(response.data["elements"][1]["order"], 2)
        self.assertEqual(response.data["elements"][1]["type"], "nuggets")
        self.assertEqual(response.data["elements"][2]["order"], 3)
        self.assertEqual(response.data["elements"][2]["type"], "menus")

    def test_put_structure_duplicate_round_error(self):
        """Erreur si le même type de manche apparaît deux fois."""
        payload = {
            "elements": [
                {"type": "nuggets", "id": _element_id_for_slug(self.bq, "nuggets")},
                {"type": "nuggets", "id": _element_id_for_slug(self.bq, "nuggets")},
            ]
        }

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_any_nuggets_allowed(self):
        """Une manche peut référencer n'importe quel Nuggets (plus de FK sur BurgerQuiz)."""
        bq_empty = BurgerQuizFactory.create(title="Quiz vide")
        other_bq = BurgerQuizFactory.create_full(title="Autre quiz")
        payload = {
            "elements": [
                {"type": "nuggets", "id": _element_id_for_slug(other_bq, "nuggets")},
            ]
        }

        response = self.client.put(
            reverse("burger-quiz-structure", kwargs={"pk": bq_empty.pk}),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BurgerQuizElement.objects.filter(burger_quiz=bq_empty).count(), 1)

    def test_put_structure_interlude_not_found_error(self):
        """Erreur si un interlude référencé n'existe pas."""
        payload = {
            "elements": [
                {"type": "video_interlude", "id": str(uuid.uuid4())},
                {"type": "nuggets", "id": _element_id_for_slug(self.bq, "nuggets")},
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
        """Structure vide : plus de lignes ; lecture suivante = []."""
        payload = {"elements": []}

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["elements"], [])

        get_response = self.client.get(self.url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.data["elements"]), 0)

    def test_put_structure_multiple_interludes_allowed(self):
        """Le même interlude vidéo peut apparaître plusieurs fois."""
        pub2 = VideoInterludeFactory.create_pub(title="Pub 2")

        payload = {
            "elements": [
                {"type": "video_interlude", "id": str(self.pub.id)},
                {"type": "nuggets", "id": _element_id_for_slug(self.bq, "nuggets")},
                {"type": "video_interlude", "id": str(pub2.id)},
                {"type": "salt_or_pepper", "id": _element_id_for_slug(self.bq, "salt_or_pepper")},
                {"type": "video_interlude", "id": str(self.pub.id)},
            ]
        }

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["elements"]), 5)


class TestBurgerQuizStructurePutValidation(APITestCase):
    """PUT /structure/ — cas d'erreur et règles de validation (alignés sur BurgerQuizStructureSerializer)."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user_val",
            email="testval@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.bq = BurgerQuizFactory.create_full(title="Quiz complet")
        self.url = reverse("burger-quiz-structure", kwargs={"pk": self.bq.pk})

    def test_put_structure_missing_elements_key(self):
        """400 si le corps ne contient pas la clé `elements`."""
        response = self.client.put(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("elements", response.data)

    def test_put_structure_elements_not_a_list(self):
        """400 si `elements` n'est pas une liste."""
        response = self.client.put(self.url, {"elements": {}}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_element_not_an_object(self):
        """400 si un élément du tableau n'est pas un objet."""
        response = self.client.put(self.url, {"elements": ["invalid"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_unknown_type(self):
        """400 si `type` n'est pas un slug connu."""
        response = self.client.put(
            self.url,
            {"elements": [{"type": "unknown_round", "id": str(uuid.uuid4())}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_missing_type(self):
        """400 si `type` est absent."""
        response = self.client.put(
            self.url,
            {"elements": [{"id": str(_element_id_for_slug(self.bq, "nuggets"))}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_missing_id(self):
        """400 si `id` est absent pour une manche."""
        response = self.client.put(
            self.url,
            {"elements": [{"type": "nuggets"}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_invalid_uuid(self):
        """400 si `id` n'est pas un UUID valide."""
        response = self.client.put(
            self.url,
            {"elements": [{"type": "nuggets", "id": "not-a-uuid"}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_id_wrong_model_for_type(self):
        """400 si l'id existe pour une autre ressource que celle indiquée par `type`."""
        nuggets_id = _element_id_for_slug(self.bq, "nuggets")
        response = self.client.put(
            self.url,
            {"elements": [{"type": "salt_or_pepper", "id": nuggets_id}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_video_interlude_id_is_not_interlude(self):
        """400 si type=video_interlude mais l'id n'est pas un VideoInterlude."""
        nuggets_id = _element_id_for_slug(self.bq, "nuggets")
        response = self.client.put(
            self.url,
            {"elements": [{"type": "video_interlude", "id": nuggets_id}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_structure_round_id_not_found(self):
        """400 si aucune manche du type demandé n'existe pour cet id."""
        response = self.client.put(
            self.url,
            {"elements": [{"type": "nuggets", "id": str(uuid.uuid4())}]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
