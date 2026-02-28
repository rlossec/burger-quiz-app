# python manage.py test quiz.tests.interludes.test_delete
# DELETE /api/quiz/interludes/{id}/ — Suppression d'un interlude vidéo.

import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...models import VideoInterlude
from ..factories import (
    VideoInterludeFactory,
    BurgerQuizFactory,
    BurgerQuizElementFactory,
)

User = get_user_model()


class TestInterludeDeleteEndpoint(APITestCase):
    """DELETE /api/quiz/interludes/{id}/ — Suppression d'un interlude."""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)
        self.interlude = VideoInterludeFactory.create_intro(title="Intro à supprimer")
        self.url = reverse("interlude-detail", kwargs={"pk": self.interlude.pk})

    def test_delete_interlude_success(self):
        """Suppression réussie d'un interlude non utilisé."""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(VideoInterlude.objects.filter(pk=self.interlude.pk).exists())

    def test_delete_interlude_not_found(self):
        """404 si l'interlude n'existe pas."""
        url = reverse("interlude-detail", kwargs={"pk": uuid.uuid4()})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_interlude_in_use(self):
        """
        Erreur si l'interlude est utilisé dans un Burger Quiz.
        
        Note: Ce test dépend de la politique de suppression choisie.
        Si on autorise la suppression en cascade, ce test devra être adapté.
        """
        bq = BurgerQuizFactory.create_full(title="Quiz avec interlude")
        BurgerQuizElementFactory.create_interlude(
            burger_quiz=bq,
            order=1,
            interlude=self.interlude,
        )
        
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(VideoInterlude.objects.filter(pk=self.interlude.pk).exists())
