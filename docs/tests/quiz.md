# Tests du module Quiz

Ce document décrit les tests des endpoints du module `quiz` (questions, manches, Burger Quiz), alignés sur les spécifications **`docs/backend/api-endpoints-et-contraintes.md`** et **`docs/api-reference.md`**.

## Exécution des tests

Tous les tests du module quiz :

```bash
uv run manage.py test quiz.tests
```

Avec Docker (depuis la racine du projet, `manage.py` dans `backend/src`) :

```bash
docker compose exec backend uv run python manage.py test quiz.tests
```

---

## Structure des tests

Les tests sont organisés en **dossiers par famille** avec **un fichier par endpoint**.

Les données de test du quiz sont créées via des **factories** (factory_boy). La liste des factories, leurs méthodes et des exemples d’usage sont décrits dans un fichier dédié :

→ **[Factories Quiz — liste et fonctionnement](quiz-factories.md)**

---

## Détail par ressource

### Questions

- **Dossier** : `quiz/tests/questions/`
- **Exécution** : `uv run manage.py test quiz.tests.questions`

| Endpoint                        | Fichier          | Nb Tests | Lien                                               |
| ------------------------------- | ---------------- | -------- | -------------------------------------------------- |
| `GET /api/quiz/questions/`      | `test_list.py`   | 4        | [Liste des questions](#liste-des-questions)        |
| `GET /api/quiz/questions/<id>/` | `test_detail.py` | 2        | [Détail d'une question](#détail-dune-question)     |
| `POST /api/quiz/questions/`     | `test_create.py` | 15       | [Création d'une question](#création-dune-question) |

#### Liste des questions

**Endpoint** : `GET /api/quiz/questions/`
Body : Aucun
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

**Légende Avancement** : 🔲 Skip | 🟡 Failed | 🟢 Passed — **Status** : 🟢 200

|   # | Endpoint (URL + filtres)                                      | Status | Description                                                                                                                     | Avancement |
| --: | ------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- | ---------- |
|   1 | `GET /api/quiz/questions/`                                    | 🟢 200 | Cas simple de succès ; liste complète, champs exposés (id, text, question_type, original, usage_count, created_at, updated_at). | 🟡         |
|   2 | `GET /api/quiz/questions/`                                    | 🟢 200 | Champ calculé `usage_count` présent sur chaque question (test actuellement skip).                                               | 🔲         |
|   3 | `GET /api/quiz/questions/?question_type=<type>`               | 🟢 200 | Test paramétré (sous-tests NU, SP, ME, AD, DB) : seules les questions du type demandé sont renvoyées.                           | 🟡         |
|   4 | `GET /api/quiz/questions/?original=true` \| `?original=false` | 🟢 200 | Deux sous-tests : seules les questions avec `original=true` ou `original=false` selon le paramètre.                             | 🟡         |

#### Détail d'une question

**Endpoint** : `GET /api/quiz/questions/<id>/`  
Body : Aucun

Réponse attendue :

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
| --: | ----------------------------------------------- | ------ | -------------------------------------------------- | ---------- |
|   1 | `GET /api/quiz/questions/<id>/` (id existant)   | 🟢 200 | Succès ; champs id, text, question_type, original. | 🟡         |
|   2 | `GET /api/quiz/questions/<id>/` (id inexistant) | 🔴 404 | Not Found.                                         | 🟡         |

#### Création d'une question

**Endpoint** : `POST /api/quiz/questions/`  
**Body** :

```json
{
  ## obligatoire
  "text": "intitulé de la question",
  "question_type": "Type de la question parmi NU, SP, ME, AD, DB",
  ## optionnel mais requis pour certain type de question
  "answers": [
    {"text": "Paris", "is_correct": true},
    {"text": "Lyon", "is_correct": false},
    {"text": "Marseille", "is_correct": false},
    {"text": "Toulouse", "is_correct": false}
  ],
  ## optionnel
  "video_url": "url d'une vidéo pour la question",
  "audio_url": "url d'un audio pour la question",
  "original": "Spécifié si faux"
}
```

**Contraintes par type** (réponses `answers` selon le type) :

| Type                       | Règle                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **NU** (Nuggets)           | 4 réponses proposées, **une seule** valide (`is_correct=true`) et 3 leurres.                                  |
| **SP** (Sel ou poivre)     | Plusieurs réponses exactes possibles ; pas de leurres (plusieurs `is_correct=true` autorisés).                |
| **ME** (Menu)              | Une réponse exacte possible ; pas de leurres (`is_correct=true` sur une réponse).                             |
| **AD** (Addition)          | Une réponse exacte ou pas de réponse possible ; pas de leurres. Si `answers` fournies, au moins une correcte. |
| **DB** (Burger de la mort) | **Pas de réponses** : `answers` absentes ou tableau vide.                                                     |

**Légende Avancement** : 🔲 Skip | 🟡 Failed | 🟢 Passed — **Status** : 🟢 201 | 🔴 400

|   # | Cas                                                 | Status | Description                                          | Avancement |
| --: | --------------------------------------------------- | ------ | ---------------------------------------------------- | ---------- |
|   1 | `POST` NU payload valide (4 réponses, 1 is_correct) | 🟢 201 | Création OK ; question + 4 answers en BDD.           | 🟡         |
|   2 | `POST` avec video_url et audio_url                  | 🟢 201 | Champs optionnels enregistrés.                       | 🟡         |
|   3 | `POST` sans `text`                                  | 🔴 400 | Champ text requis.                                   | 🟡         |
|   4 | `POST` sans `question_type`                         | 🔴 400 | Champ question_type requis.                          | 🟡         |
|   5 | `POST` NU, SP, ME ou AD sans `answers`              | 🔴 400 | answers requis pour ces types.                       | 🟡         |
|   6 | `POST` DB avec `answers` vide                       | 🟢 201 | DB ne requiert pas de réponses.                      | 🟡         |
|   7 | `POST` NU avec nombre de réponses ≠ 4 (1 ou 5)      | 🔴 400 | Exactement 4 réponses pour NU.                       | 🟡         |
|   8 | `POST` NU sans aucune `is_correct=true`             | 🔴 400 | Une réponse correcte requise pour NU.                | 🟡         |
|   9 | `POST` NU avec plusieurs `is_correct=true`          | 🔴 400 | Une seule réponse correcte pour NU.                  | 🟡         |
|  10 | `POST` SP avec plusieurs `is_correct=true`          | 🟢 201 | Autorisé pour SP.                                    | 🟡         |
|  11 | `POST` ME avec une réponse is_correct=true          | 🟢 201 | Création OK.                                         | 🟡         |
|  12 | `POST` AD avec une réponse correcte                 | 🟢 201 | Création OK.                                         | 🟡         |
|  13 | `POST` AD avec toutes les réponses incorrectes      | 🔴 400 | Au moins une is_correct requise si answers fournies. | 🟡         |
|  14 | `POST` DB avec réponses fournies                    | 🔴 400 | DB ne doit pas accepter answers.                     | 🟡         |
|  15 | `POST` question_type invalide (ex. `XX`)            | 🔴 400 | Validation enum.                                     | 🟡         |

_Référence des noms de tests_ : 1 → `test_create_nuggets_success` ; 2 → `test_create_accepts_video_url_audio_url` ; 3 → `test_create_missing_text_returns_400` ; 4 → `test_create_missing_question_type_returns_400` ; 5 → `test_create_requires_answers_for_nu_sp_me_ad` ; 6 → `test_create_db_success_empty_answers` ; 7 → `test_create_nuggets_not_four_answers_returns_400` ; 8 → `test_create_nuggets_no_correct_answer_returns_400` ; 9 → `test_create_nuggets_multiple_correct_returns_400` ; 10 → `test_create_sp_success` ; 11 → `test_create_me_success` ; 12 → `test_create_ad_success` ; 13 → `test_create_ad_all_incorrect_returns_400` ; 14 → `test_create_db_with_answers_returns_400` ; 15 → `test_create_invalid_question_type_returns_400`.

_Tests non implémentés (à ajouter si règle métier)_ : answers en doublon → 400 ; limite max de réponses (ex. 10) → 400 ; transaction rollback si erreur sur answers.

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
