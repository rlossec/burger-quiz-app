# Tests du module Quiz

Ce document décrit les tests des endpoints du module `quiz` (questions, manches, Burger Quiz), alignés sur la spécification **`docs/backend/api-reference.md`**.

## Exécution des tests

Tous les tests du module quiz :

```bash
uv run manage.py test quiz.tests # Depuis backend/src
docker compose exec backend uv run python manage.py test quiz.tests # Avec Docker
```

**Rapport HTML** : à chaque exécution des tests, un rapport est généré dans `backend/src/reports/test-report.html` (résumé : succès / échecs / ignorés, détail des erreurs). Ouvrir ce fichier dans un navigateur pour consulter le bilan.

---

## Structure des tests

Les tests sont organisés en dossiers par **ressources** avec **un fichier par type d'endpoint**.

```
quiz/tests/
├── mixins/                      # Mixins réutilisables
│   ├── __init__.py
│   ├── base.py                  # ResourceTestMixin (base)
│   ├── auth.py                  # AuthRequiredMixin
│   ├── author.py                # AuthorAutoAssignOnCreateMixin, etc.
│   ├── tags.py                  # TagsOnCreateMixin, etc.
│   └── timestamps.py            # TimestampsInDetailResponseMixin, etc.
├── factories.py                 # Factories (factory_boy)
├── __init__.py                  # Constantes partagées
├── questions/
│   ├── test_list.py
│   ├── test_detail.py
│   ├── test_create.py
│   ├── test_update.py
│   └── test_delete.py
├── salt_or_pepper/
│   ├── test_list.py
│   ├── test_detail.py
│   ├── test_create.py
│   └── test_update.py
└── ... (autres ressources)
```

### Principe

Les tests métier spécifiques restent dans chaque fichier (`test_create.py`, `test_list.py`, etc.). Les tests des champs communs (`author`, `tags`, `timestamps`, `auth`) sont ajoutés via **des mixins** importés depuis `quiz/tests/mixins/`.

**Avantages** :

- Un seul fichier par endpoint, tout au même endroit
- Tests uniformes sur toutes les ressources
- Exécution par ressource : `uv run manage.py test quiz.tests.salt_or_pepper`
- Exécution ciblée : `uv run manage.py test quiz.tests.salt_or_pepper.test_create`

---

## Mixins disponibles

### Dossier `quiz/tests/mixins/`

| Fichier         | Mixin                             | Usage (fichier cible) |
| --------------- | --------------------------------- | --------------------- |
| `auth.py`       | `AuthRequiredMixin`               | `test_list.py`        |
| `author.py`     | `AuthorAutoAssignOnCreateMixin`   | `test_create.py`      |
| `author.py`     | `AuthorReadOnlyOnCreateMixin`     | `test_create.py`      |
| `author.py`     | `AuthorInDetailResponseMixin`     | `test_detail.py`      |
| `author.py`     | `AuthorInListResponseMixin`       | `test_list.py`        |
| `author.py`     | `AuthorFilterMixin`               | `test_list.py`        |
| `author.py`     | `AuthorNotChangedOnUpdateMixin`   | `test_update.py`      |
| `tags.py`       | `TagsOnCreateMixin`               | `test_create.py`      |
| `tags.py`       | `TagsInDetailResponseMixin`       | `test_detail.py`      |
| `tags.py`       | `TagsInListResponseMixin`         | `test_list.py`        |
| `tags.py`       | `TagsFilterMixin`                 | `test_list.py`        |
| `tags.py`       | `TagsUpdateMixin`                 | `test_update.py`      |
| `timestamps.py` | `TimestampsInDetailResponseMixin` | `test_detail.py`      |
| `timestamps.py` | `TimestampsInListResponseMixin`   | `test_list.py`        |
| `timestamps.py` | `TimestampsReadOnlyMixin`         | `test_create.py`      |

### Exemple d'utilisation

```python
# quiz/tests/salt_or_pepper/test_create.py

from rest_framework.test import APITestCase
from ..factories import SaltOrPepperFactory, QuestionFactory
from ..mixins import (
    AuthorAutoAssignOnCreateMixin,
    AuthorReadOnlyOnCreateMixin,
    TagsOnCreateMixin,
    TimestampsReadOnlyMixin,
)

# Tests métier existants
class TestSaltOrPepperCreateEndpoint(APITestCase):
    def test_create_salt_or_pepper_success(self):
        ...

# Tests author via mixin
class TestSaltOrPepperCreateAuthor(
    AuthorAutoAssignOnCreateMixin,
    AuthorReadOnlyOnCreateMixin,
    APITestCase,
):
    factory = SaltOrPepperFactory
    url_basename = "salt-or-pepper"

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(...)
        self.client.force_authenticate(user=self.user)
        self.q1 = QuestionFactory.create_sp("SP1")

    def get_valid_payload(self):
        return {"title": "Test", "propositions": ["A", "B"], "question_ids": [str(self.q1.id)]}
```

### Configuration des mixins

Chaque mixin attend certains attributs :

| Attribut              | Description                                | Requis par                    |
| --------------------- | ------------------------------------------ | ----------------------------- |
| `factory`             | Factory pour créer des instances           | Tous sauf `AuthRequiredMixin` |
| `url_basename`        | Basename de l'URL (ex: `"salt-or-pepper"`) | Tous                          |
| `self.user`           | Utilisateur authentifié (dans `setUp`)     | Tous sauf `AuthRequiredMixin` |
| `get_valid_payload()` | Méthode retournant un payload valide       | Create, Update                |

---

## Factories

Les données de test sont créées via **factory_boy**. Documentation complète :

→ **[Factories Quiz](quiz-factories.md)**

---

## Détail par ressource

### Questions (`/api/quiz/questions/`)

**Dossier** : `quiz/tests/questions/`
**Exécution** : `uv run manage.py test quiz.tests.questions`

| Fichier          | Tests                                   |
| ---------------- | --------------------------------------- |
| `test_list.py`   | Liste, filtres (type, original, search) |
| `test_detail.py` | Détail, 404                             |
| `test_create.py` | Création, validation, règles par type   |
| `test_update.py` | Mise à jour, validation                 |
| `test_delete.py` | Suppression, cascade                    |

---

### Nuggets (`/api/quiz/nuggets/`)

**Dossier** : `quiz/tests/nuggets/`
**Exécution** : `uv run manage.py test quiz.tests.nuggets`

---

### Sel ou poivre (`/api/quiz/salt-or-pepper/`)

**Dossier** : `quiz/tests/salt_or_pepper/`
**Exécution** : `uv run manage.py test quiz.tests.salt_or_pepper`

| Fichier          | Tests métier                      | Tests via mixins               |
| ---------------- | --------------------------------- | ------------------------------ |
| `test_list.py`   | Liste                             | Auth, Author, Tags, Timestamps |
| `test_detail.py` | Détail, 404                       | Author, Tags, Timestamps       |
| `test_create.py` | Création, validation propositions | Author, Tags, Timestamps       |
| `test_update.py` | PATCH titre                       | Author, Tags                   |

---

### Thèmes de menu (`/api/quiz/menu-themes/`)

**Dossier** : `quiz/tests/menu_themes/`
**Exécution** : `uv run manage.py test quiz.tests.menu_themes`

---

### Manche Menus (`/api/quiz/menus/`)

**Dossier** : `quiz/tests/menus/`
**Exécution** : `uv run manage.py test quiz.tests.menus`

---

### Addition (`/api/quiz/additions/`)

**Dossier** : `quiz/tests/additions/`
**Exécution** : `uv run manage.py test quiz.tests.additions`

---

### Burger de la mort (`/api/quiz/deadly-burgers/`)

**Dossier** : `quiz/tests/deadly_burgers/`
**Exécution** : `uv run manage.py test quiz.tests.deadly_burgers`

---

### Burger Quiz (`/api/quiz/burger-quizzes/`)

**Dossier** : `quiz/tests/burger_quizzes/`
**Exécution** : `uv run manage.py test quiz.tests.burger_quizzes`

---

## Divers

### Constantes partagées (`quiz/tests/__init__.py`)

Messages d'erreur DRF et métier, types de questions, types de menus.

### URLs et vues factices

Pour que les tests puissent appeler `reverse()` sur les noms d'URL du quiz, le module `quiz` expose des routes via `quiz/urls.py` et un `PlaceholderViewSet` dans `quiz/views.py`. Lors de l'implémentation réelle des endpoints, remplacer ce viewset par les ViewSets métier ; les tests restent inchangés et valideront le comportement attendu.
