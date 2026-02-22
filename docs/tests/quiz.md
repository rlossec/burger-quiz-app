# Tests du module Quiz

Ce document décrit les tests des endpoints du module `quiz` (questions, manches, Burger Quiz), alignés sur la spécification **`docs/backend/api-reference.md`**.

## Exécution des tests

Tous les tests du module quiz :

```bash
uv run manage.py test quiz.tests # Depuis backend/src
docker compose exec backend uv run python manage.py test quiz.tests # Avec Docker
```

---

## Structure des tests

Les tests sont organisés en dossiers par **modules** puis par **ressources** avec **un fichier par endpoint**.

Les données de test du quiz sont créées via des **factories** (factory_boy). La liste des factories, leurs méthodes et des exemples d’usage sont décrits dans un fichier dédié :

→ **[Factories Quiz](quiz-factories.md)**

---

## Détail par ressource

### Questions

- **Dossier** : `quiz/tests/questions/`
- **Exécution** : `uv run manage.py test quiz.tests.questions`

| Endpoint                        | Fichier          | Nb Tests | Lien                                               |
| ------------------------------- | ---------------- | -------- | -------------------------------------------------- |
| `GET /api/quiz/questions/`      | `test_list.py`   | 4        | [Liste des questions](#liste-des-questions)        |
| `GET /api/quiz/questions/<id>/` | `test_detail.py` | 2        | [Détail d'une question](#détail-dune-question)     |
| `POST /api/quiz/questions/`     | `test_create.py` | 19       | [Création d'une question](#création-dune-question) |
| `PUT /api/quiz/questions/<id>/`  | `test_update.py` | 19       | [Mise à jour d'une question](#mise-à-jour-dune-question) |
| `DELETE /api/quiz/questions/<id>/` | `test_delete.py` | 2     | [Suppression d'une question](#suppression-dune-question) |

#### Liste des questions

**Endpoint** : `GET /api/quiz/questions/`
**Body** : Aucun
**Réponse attendue** :

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "c8d5d5c0-1234-4b8f-9c2a-111111111111",
      "text": "Question Nuggets",
      "question_type": "NU",
      "original": false,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
      "text": "Question SP",
      "question_type": "SP",
      "original": true,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-02T09:30:00Z",
      "updated_at": "2025-01-02T09:30:00Z"
    }
  ]
}
```

**Légende Avancement** : 🔲 Skip | 🟡 Failed | 🟢 Passed

|   # | Endpoint (URL + filtres)                                      | Status | Description                                                                                                                     | Avancement |
| --: | ------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- | ---------- |
|   1 | `GET /api/quiz/questions/`                                    | 🟢 200 | Test du succès, avec les champs attendus | 🟡         |
|   2 | `GET /api/quiz/questions/`                                    | 🟢 200 | Test du champ usage_count                                               | 🔲         |
|   3 | `GET /api/quiz/questions/?question_type=<type>`               | 🟢 200 | Test du filtre type avec sous tests pour NU, SP, ME, AD, DB.                           | 🟡         |
|   4 | `GET /api/quiz/questions/?original=true` \| `?original=false` | 🟢 200 | Test du filtre original.                             | 🟡         |

#### Détail d'une question

**Endpoint** : `GET /api/quiz/questions/<id>/`  
**Body** : Aucun  
**Réponse attendue** :

```json
{
  "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
  "text": "Question SP",
  "question_type": "SP",
  "original": true,
  "explanations": "Explications",
  "video_url": "https://video.com",
  "image_url": "https://image.com",
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "answers": [
    { "text": "Paris", "is_correct": true },
    { "text": "Lyon", "is_correct": false },
    { "text": "Marseille", "is_correct": false },
    { "text": "Toulouse", "is_correct": false }
  ]
}
```

**Légende Avancement** : 🔲 Skip | 🟡 Failed | 🟢 Passed —

|   # | Cas                                             | Status | Description                                        | Avancement |
| ---: | ----------------------------------------------- | ------ | -------------------------------------------------- | ---------- |
|   1 | `GET /api/quiz/questions/<id>/` (id existant)   | 🟢 200 | Succès | 🟡         |
|   2 | `GET /api/quiz/questions/<id>/` (id inexistant) | 🔴 404 | Id Not Found.                                         | 🟡         |

#### Création d'une question

**Endpoint** : `POST /api/quiz/questions/`  
**Fichier** : `quiz/tests/questions/test_create.py`

**Structure des tests** :

- **Classe de base** : **`QuestionCreateBaseTestCase`** (hérite de `APITestCase`) — fournit `setUp()` (url), `build_payload()`, `post()`, `assertCreated()`, `assertBadRequest()`. Toutes les classes de test en héritent.
- **Contraintes communes** (une seule classe, sous-tests par type) :
  - **`TestQuestionCreateValidation`** : champs obligatoires, video_url/image_url, answers obligatoires pour les types à réponses, et interdiction des réponses incorrectes pour les types ouverts.
    - `test_missing_text_returns_400` (sous-test par type : NU, SP, ME, AD, DB).
    - `test_empty_text_returns_400` (texte vide ou uniquement espaces → 400 ; sous-tests « vide », « espaces »).
    - `test_missing_question_type_returns_400` (sous-test par type).
    - `test_invalid_question_type_returns_400` (question_type invalide, ex. `XX`).
    - `test_video_url_and_image_url_are_saved` (sous-test par type).
    - `test_invalid_video_url_returns_400` (video_url doit être une URL valide ; sous-test par type).
    - `test_invalid_image_url_returns_400` (image_url doit être une URL valide ; sous-test par type).
    - `test_incorrect_answer_forbidden_for_open_types` (SP, ME, AD : une réponse `is_correct=false` → 400 ; sous-tests).
    - `test_missing_answers_returns_400_for_types_that_require_them` (NU, SP, ME, AD sans `answers` → 400 ; sous-tests).
- **Classes par type de question** (héritent de `QuestionCreateBaseTestCase`) :
  - **`TestQuestionCreateNU`** : `test_create_success`, `test_wrong_number_of_answers_returns_400`, `test_no_correct_answer_returns_400`, `test_multiple_correct_answers_returns_400`.
  - **`TestQuestionCreateSP`** : `test_create_success`.
  - **`TestQuestionCreateME`** : `test_create_success`.
  - **`TestQuestionCreateAD`** : `test_create_success`, `test_all_incorrect_answers_returns_400`.
  - **`TestQuestionCreateDB`** : `test_create_success_without_answers`, `test_create_with_answers_returns_400`.

**Body** :

```json
{
  "text": "intitulé de la question",
  "question_type": "NU | SP | ME | AD | DB",
  "original": false,
  "answers": [ {"text": "...", "is_correct": true/false}, ... ],
  "video_url": "url optionnelle",
  "image_url": "url optionnelle"
}
```

**Contraintes par type** (réponses `answers` selon le type) :

| Type                       | Règle                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **NU** (Nuggets)           | 4 réponses proposées, **une seule** valide (`is_correct=true`) et 3 leurres.                                  |
| **SP** (Sel ou poivre)     | Questions ouvertes : toutes les réponses doivent être correctes (`is_correct=true`) ; pas de proposition piège. |
| **ME** (Menu)              | Questions ouvertes : une réponse, obligatoirement correcte (`is_correct=true`) ; pas de piège.                  |
| **AD** (Addition)          | Questions ouvertes : si `answers` fournies, toutes correctes ; au moins une requise. Pas de piège.           |
| **DB** (Burger de la mort) | **Pas de réponses** : `answers` absentes ou tableau vide.                                                     |

**Légende Avancement** : 🔲 Skip | 🟡 Failed | 🟢 Passed — **Status** : 🟢 201 | 🔴 400

|   # | Cas                                                 | Status | Classe / test                                                       | Avancement |
| --: | --------------------------------------------------- | ------ | -------------------------------------------------------------------- | ---------- |
|   1 | `POST` NU payload valide (4 réponses, 1 is_correct) | 🟢 201 | `TestQuestionCreateNU.test_create_success`                           | 🟡         |
|   2 | `POST` avec video_url et image_url (tous types)    | 🟢 201 | `TestQuestionCreateValidation.test_video_url_and_image_url_are_saved` | 🟡         |
|   3 | `POST` sans `text` (NU, SP, ME, AD, DB)             | 🔴 400 | `TestQuestionCreateValidation.test_missing_text_returns_400`         | 🟡         |
|   4 | `POST` avec `text` vide ou espaces seuls            | 🔴 400 | `TestQuestionCreateValidation.test_empty_text_returns_400`            | 🟡         |
|   5 | `POST` sans `question_type` (NU, SP, ME, AD, DB)   | 🔴 400 | `TestQuestionCreateValidation.test_missing_question_type_returns_400` | 🟡         |
|   6 | `POST` avec video_url invalide (tous types)        | 🔴 400 | `TestQuestionCreateValidation.test_invalid_video_url_returns_400`      | 🟡         |
|   7 | `POST` avec image_url invalide (tous types)         | 🔴 400 | `TestQuestionCreateValidation.test_invalid_image_url_returns_400`     | 🟡         |
|   8 | `POST` NU, SP, ME ou AD sans `answers`              | 🔴 400 | `TestQuestionCreateValidation.test_missing_answers_returns_400_for_types_that_require_them` | 🟡         |
|   9 | `POST` DB avec `answers` vide                       | 🟢 201 | `TestQuestionCreateDB.test_create_success_without_answers`          | 🟡         |
|  10 | `POST` NU avec nombre de réponses ≠ 4 (1 ou 5)      | 🔴 400 | `TestQuestionCreateNU.test_wrong_number_of_answers_returns_400`     | 🟡         |
|  11 | `POST` NU sans aucune `is_correct=true`             | 🔴 400 | `TestQuestionCreateNU.test_no_correct_answer_returns_400`             | 🟡         |
|  12 | `POST` NU avec plusieurs `is_correct=true`         | 🔴 400 | `TestQuestionCreateNU.test_multiple_correct_answers_returns_400`     | 🟡         |
|  13 | `POST` SP avec plusieurs `is_correct=true`         | 🟢 201 | `TestQuestionCreateSP.test_create_success`                           | 🟡         |
|  14 | `POST` ME avec une réponse is_correct=true          | 🟢 201 | `TestQuestionCreateME.test_create_success`                           | 🟡         |
|  15 | `POST` AD avec une réponse correcte                 | 🟢 201 | `TestQuestionCreateAD.test_create_success`                          | 🟡         |
|  16 | `POST` AD sans bonne réponse                        | 🔴 400 | `TestQuestionCreateAD.test_all_incorrect_answers_returns_400`        | 🟡         |
|  17 | `POST` DB avec réponses fournies                    | 🔴 400 | `TestQuestionCreateDB.test_create_with_answers_returns_400`         | 🟡         |
|  18 | `POST` question_type invalide (ex. `XX`)            | 🔴 400 | `TestQuestionCreateValidation.test_invalid_question_type_returns_400` | 🟡         |
|  19 | `POST` SP, ME ou AD avec une réponse `is_correct=false` (piège) | 🔴 400 | `TestQuestionCreateValidation.test_incorrect_answer_forbidden_for_open_types` | 🟡         |

_Tests non implémentés (à ajouter si règle métier)_ : answers en doublon → 400 ; limite max de réponses (ex. 10) → 400 ; transaction rollback si erreur sur answers.

#### Mise à jour d'une question

**Endpoint** : `PUT /api/quiz/questions/<id>/`  
**Fichier** : `quiz/tests/questions/test_update.py`

Les tests de mise à jour reprennent les **mêmes contraintes** que la création (validation des champs, règles par type). On envoie un payload complet (PUT) et on vérifie 200 OK ou 400 selon le cas.

**Structure des tests** :

- **Classe de base** : **`QuestionUpdateBaseTestCase`** — fournit une question existante, `self.url` (détail), `put(payload)`, `assertOk`, `assertBadRequest`.
- **Contraintes communes** : **`TestQuestionUpdateValidation`** — mêmes tests que pour la création (text manquant/vide, question_type manquant/invalide, video_url/image_url valides ou invalides, réponses incorrectes interdites pour SP/ME/AD, answers obligatoires pour NU/SP/ME/AD).
- **Classes par type** : **`TestQuestionUpdateNU`**, **`TestQuestionUpdateSP`**, **`TestQuestionUpdateME`**, **`TestQuestionUpdateAD`**, **`TestQuestionUpdateDB`** — succès de mise à jour et contraintes spécifiques (nombre de réponses NU, pièges interdits, etc.).

|   # | Cas | Status | Classe / test |
| --: | --- | ------ | -------------- |
|   1 | `PUT` avec payload valide (par type) | 🟢 200 | `TestQuestionUpdateNU/SP/ME/AD/DB.test_update_success*` |
|   2 | `PUT` avec les mêmes validations qu’en création (text, question_type, URLs, answers) | 🔴 400 | `TestQuestionUpdateValidation.*` |
|   3 | `PUT` NU/SP/ME/AD/DB contraintes spécifiques (ex. NU pas 4 réponses, DB avec answers) | 🔴 400 | Classes par type `test_*_returns_400` |

#### Suppression d'une question

**Endpoint** : `DELETE /api/quiz/questions/<id>/`  
**Fichier** : `quiz/tests/questions/test_delete.py`

|   # | Cas | Status | Classe / test |
| --: | --- | ------ | -------------- |
|   1 | `DELETE` avec id inexistant | 🔴 404 | `TestQuestionDeleteEndpoint.test_delete_unknown_id_returns_404` |
|   2 | `DELETE` supprime la question et les réponses en cascade | 🟢 204 | `TestQuestionDeleteEndpoint.test_delete_question_removes_answers_in_cascade` |

---

### Nuggets (`/api/quiz/nuggets/`)

**Dossier** : `quiz/tests/nuggets/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Sel ou poivre (`/api/quiz/salt-or-pepper/`)

**Dossier** : `quiz/tests/salt_or_pepper/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Thèmes de menu (`/api/quiz/menu-themes/`)

**Dossier** : `quiz/tests/menu_themes/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Manche Menus (`/api/quiz/menus/`)

**Dossier** : `quiz/tests/menus/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Addition (`/api/quiz/additions/`)

**Dossier** : `quiz/tests/additions/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Burger de la mort (`/api/quiz/deadly-burgers/`)

**Dossier** : `quiz/tests/deadly_burgers/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**
- **`test_update.py`**

---

### Burger Quiz (`/api/quiz/burger-quizzes/`)

**Dossier** : `quiz/tests/burger_quizzes/`

- **`test_list.py`**
- **`test_detail.py`**
- **`test_create.py`**

---

## Divers

##### Constantes partagées (`quiz/tests/__init__.py`)

##### URLs et vues factices

Pour que les tests puissent appeler `reverse()` sur les noms d’URL du quiz, le module `quiz` expose des routes via `quiz/urls.py` et un `PlaceholderViewSet` dans `quiz/views.py`. Lors de l’implémentation réelle des endpoints, remplacer ce viewset par les ViewSets métier ; les tests restent inchangés et valideront le comportement attendu.
