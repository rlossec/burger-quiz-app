# Référence API Burger Quiz

Ce document décrit les endpoints de l’API Burger Quiz par app Django :
 - **Accounts** (authentification et utilisateurs)
 - **Quiz** (manches, questions, Burger Quiz).

## 0. Général

### 0.1. Bases

**Base URL** : `/api/`

### 0.2. Authentification

**Authentification** : JWT Bearer. En-tête : `Authorization: Bearer <access_token>`.  
Pour obtenir un token : `POST /api/auth/jwt/create/`.

### 0.3. Permissions

TODO

## 1. Accounts

Tous les endpoints Accounts sont préfixés par **`/api/auth/`**.

### 1.1 JWT

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/jwt/create/` | Créer un couple access/refresh à partir d’identifiants |
| `POST` | `/api/auth/jwt/refresh/` | Rafraîchir l’access token avec le refresh token |
| `POST` | `/api/auth/jwt/verify/` | Vérifier la validité d’un token |

#### 1.1.1. Login

**Endpoint** : `POST /api/auth/jwt/create/`
**Authentification**: AllowAny
**Body** :
```json
{
  "username": "string",
  "password": "string"
}
```

- `username` : obligatoire  
- `password` : obligatoire  

**Réponse Attendue** : 200
```json
{
  "access": "string",
  "refresh": "string"
}
```

> Utiliser `access` dans l’en-tête `Authorization: Bearer <access>` pour les requêtes authentifiées.

#### 1.1.2. Refresh de token

**Endpoint**: `POST /api/auth/jwt/refresh/`
**Authentification**: AllowAny
**Body** :
```json
{
  "refresh": "string"
}
```

**Réponse Attendue** : Status 200
```json
{
  "access": "string",
  "refresh": "string"
}
```

#### 1.1.3. Vérification de token

**Endpoint**: `POST /api/auth/jwt/verify/`
**Authentification**: AllowAny
**Body** :
```json
{
  "token": "string"
}
```

**Réponse Attendue** : Status 200 `{}` si le token est valide.

---

### 1.2 Utilisateurs

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/users/` | Inscription |
| `GET` | `/api/auth/users/` | Liste des utilisateurs |
| `GET` | `/api/auth/users/me/` | Utilisateur connecté (authentifié) |
| `PATCH` | `/api/auth/users/me/` | Mise à jour partielle du profil (dont avatar) |
| `GET` | `/api/auth/users/{id}/` | Détail d’un utilisateur (soi-même ou staff/superuser) |
| `PUT` | `/api/auth/users/{id}/` | Mise à jour complète (propriétaire du compte) |
| `PATCH` | `/api/auth/users/{id}/` | Mise à jour partielle (propriétaire du compte) |
| `DELETE` | `/api/auth/users/{id}/` | Suppression du compte (propriétaire ou staff selon règles métier) |

#### 1.2.1. Inscription

**Endpoint** : `POST /api/auth/users/`
**Authentification**: AllowAny
**Body** :
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securePassword123",
  "re_password": "securePassword123"
}
```

- `email` : obligatoire, unique, format email valide  
- `username` : obligatoire, unique, 150 caractères max, caractères autorisés : lettres, chiffres, @/./+/-/_  
- `password` : obligatoire (règles de complexité Django)  
- `re_password` : obligatoire, doit être égal à `password`  

**Réponse 201** : représentation de l’utilisateur (champs exposés selon le serializer, sans mot de passe). Le compte peut être inactif jusqu’à activation par email.

#### Liste des utilisateurs

**Endpoint** : `GET /api/auth/users/`
**Authentification** : isStaff
**Pagination** : 10 éléments par page (paramètres `page`, `page_size` si supportés).  

**Réponse attendue** : liste paginée d’utilisateurs avec champs : `id`, `email`, `username`, `first_name`, `last_name`, `avatar`.

#### Avoir ses informations

**Endpoint** : `GET /api/auth/users/me/`
**Authentification** : IsAuthenticated  

**Réponse attendue** : 200, info utilisateur connecté (même schéma que détail utilisateur).

#### Mise à jour de ses informations

**Endpoint** : `PATCH /api/auth/users/me/`

Mise à jour partielle du profil (dont avatar).
Champs modifiables : `email`, `first_name`, `last_name`, `avatar`.  
`id` et `username` sont en lecture seule.  

#### Detail d'un utilisateur

**Endpoint** : `GET /api/auth/users/{id}/`

- **Authentification** : isStaffOrOwner.  

**Réponse attendue** :
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "url_or_null"
}
```

#### PUT /api/auth/users/{id}/ et PATCH /api/auth/users/{id}/

Mise à jour (complète ou partielle) du compte. Réservé au propriétaire du compte. Champs modifiables : `email`, `first_name`, `last_name`, `avatar`. `id` et `username` en lecture seule. Changement d’email peut désactiver le compte jusqu’à confirmation.

#### DELETE /api/auth/users/{id}/

Suppression du compte.
Authentication : IsStaffOrOwner

---

### 1.3 Activation et réinitialisation (Djoser)

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/users/activation/` | Activer un compte (uid + token) |
| `POST` | `/api/auth/users/resend_activation/` | Renvoyer l’email d’activation |
| `POST` | `/api/auth/users/reset_password/` | Demande de réinitialisation du mot de passe (email) |
| `POST` | `/api/auth/users/reset_password_confirm/` | Confirmation (uid, token, new_password) |
| `POST` | `/api/auth/users/reset_username/` | Demande de réinitialisation du nom d’utilisateur (email) |
| `POST` | `/api/auth/users/reset_username_confirm/` | Confirmation (uid, token, new_username) |

Les schémas exacts (corps, réponses) suivent la documentation Djoser ; les tests dans `docs/tests/accounts.md` décrivent les cas de succès et d’erreur.

---

## 2. Quiz

Tous les endpoints Quiz sont préfixés par **`/api/quiz/`**.

**Vue d'ensemble du flux (création d’un Burger Quiz)**  
1. Créer les manches : Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort.  
2. Créer un Burger Quiz en fournissant un **toss** et les **IDs des manches** déjà créées.  
Les manches sont des entités indépendantes ; le Burger Quiz les référence par clé étrangère.

**Ordre recommandé des appels API**  
1. **Questions et réponses** : créer les Questions avec `question_type`, `original` (optionnel), Answers conformes au type, et optionnellement `video_url` / `image_url`.  
2. **Manches** : Nuggets (`POST /api/quiz/nuggets/`), Sel ou poivre (`POST /api/quiz/salt-or-pepper/`), Menus (3 MenuTheme puis `POST /api/quiz/menus/`), Addition (`POST /api/quiz/additions/`), Burger de la mort (`POST /api/quiz/deadly-burgers/`).  
3. **Burger Quiz** : `POST /api/quiz/burger-quizzes/` avec `title`, `toss`, et les IDs des manches (`nuggets_id`, `salt_or_pepper_id`, `menus_id`, `addition_id`, `deadly_burger_id`).

---

### 2.1 Questions et réponses

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/questions/` | Liste des questions |
| `GET` | `/api/quiz/questions/{id}/` | Détail d’une question |
| `POST` | `/api/quiz/questions/` | Création d’une question avec réponses selon le type |
| `PUT` | `/api/quiz/questions/{id}/` | Remplacement complet d’une question (idempotent) |
| `PATCH` | `/api/quiz/questions/{id}/` | Mise à jour partielle d’une question |
| `DELETE` | `/api/quiz/questions/{id}/` | Suppression d’une question |

#### 2.1.1. Liste des questions

**Endpoint** : `GET /api/quiz/questions/`

**Filtres** :
- `original` : `true` \| `false`  
- `question_type` : `NU` \| `SP` \| `ME` \| `AD` \| `DB`  
- `search` : chaîne de caractères ; recherche textuelle sur l’énoncé de la question (usage : page liste questions, modale d’ajout de questions). Combinable avec les autres filtres.  

**Champs calculés (lecture seule)** : TODO

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

#### 2.1.2. Détail d'une question

**Endpoint** : `GET /api/quiz/questions/{id}/`

**Paramètres** : aucun (ressource identifiée par `id`). Les filtres `original` et `question_type` s’appliquent à la liste (GET /api/quiz/questions/), pas au détail.

**Réponse attendue** :
```json
    {
      "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
      "text": "Question NU",
      "question_type": "NU",
      "original": true,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-02T09:30:00Z",
      "updated_at": "2025-01-02T09:30:00Z",
      "answers": [
        {"text": "Paris", "is_correct": true},
        {"text": "Lyon", "is_correct": false},
        {"text": "Marseille", "is_correct": false},
        {"text": "Toulouse", "is_correct": false}
      ]
    }
```

#### 2.1.3. Création de question

**Endpoint** : `POST /api/quiz/questions/`

**Body** :

- **Obligatoire** : `text`, **`question_type`** (NU | SP | ME | AD | DB) pour toutes les questions.
- **Requis selon le type** : `answers` obligatoire pour NU, SP, ME, AD ; absent ou tableau vide pour DB. Contraintes par type (nombre de réponses, une seule ou plusieurs correctes, pas de piège pour SP/ME/AD) — voir `docs/tests/quiz.md` et la section Quiz ci-dessous.
- **Optionnel** : `original` (booléen, défaut **`true`** = créée directement ; `false` = issue d’une émission diffusée), `video_url`, `image_url` (URLs valides), `explanations`.

```json
{
  "text": "intitulé de la question",
  "question_type": "NU",
  "original": true,
  "answers": [
    {"text": "Paris", "is_correct": true},
    {"text": "Lyon", "is_correct": false},
    {"text": "Marseille", "is_correct": false},
    {"text": "Toulouse", "is_correct": false}
  ],
  "video_url": "https://example.com/video.mp4",
  "image_url": "https://example.com/image.jpg"
}
```

**Réponse attendue** :
```json
    {
      "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
      "text": "Question NU",
      "question_type": "NU",
      "original": true,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-02T09:30:00Z",
      "updated_at": "2025-01-02T09:30:00Z",
      "answers": [
        {"text": "Paris", "is_correct": true},
        {"text": "Lyon", "is_correct": false},
        {"text": "Marseille", "is_correct": false},
        {"text": "Toulouse", "is_correct": false}
      ]
    }
```

#### 2.1.4. Mise à jour complète d'une question

**Endpoint** : `PUT /api/quiz/questions/{id}/`

**Body** (exemple) :
```json
{
  "text": "Question NU mise à jour",
  "question_type": "NU",
  "answers": [
    {"text": "Paris", "is_correct": true},
    {"text": "Lyon", "is_correct": false},
    {"text": "Marseille", "is_correct": false},
    {"text": "Toulouse", "is_correct": false}
  ],
  "video_url": "https://video.com/mise-a-jour",
  "image_url": "https://image.com/mise-a-jour",
  "original": true,
  "explanations": "Explications mises à jour"
}
```

**Réponse attendue (200)** : même forme que le détail (cf. 2.1.2), avec les champs mis à jour.

#### 2.1.5. Mise à jour partielle d'une question

**Endpoint** : `PATCH /api/quiz/questions/{id}/`

**Body** (exemple) :
```json
{
  "text": "Libellé corrigé",
  "original": false
}
```

**Réponse attendue (200)** : ressource complète de la question, avec les champs modifiés, même forme que 2.1.2.

#### 2.1.6. Suppression d'une question

**Endpoint** : `DELETE /api/quiz/questions/{id}/`

- **204 No Content** si la suppression réussit.  
- **404 Not Found** si l’`id` n’existe pas.

---

### 2.2 Manches — Nuggets

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/nuggets/` | Liste des manches Nuggets |
| `GET` | `/api/quiz/nuggets/{id}/` | Détail d’une manche Nuggets |
| `POST` | `/api/quiz/nuggets/` | Création |
| `PATCH`\| `PUT` | `/api/quiz/nuggets/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/nuggets/{id}/` | Suppression d’une manche Nuggets |

#### 2.2.1. Liste des manches Nuggets

**Endpoint** : `GET /api/quiz/nuggets/`

**Réponse attendue** :
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-nuggets-1",
      "title": "Culture générale",
      "original": false,
      "questions_count": 4,
      "burger_quiz_count": 0
    }
  ]
}
```

#### 2.2.2. Détail d'une manche Nuggets

**Endpoint** : `GET /api/quiz/nuggets/{id}/`

En **lecture**, le détail expose les **questions complètes** (et leurs réponses), et non seulement les `question_ids` :

**Réponse attendue** :
```json
{
  "id": "uuid-nuggets-1",
  "title": "Nuggets détail",
  "original": true,
  "questions_count": 4,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question Nuggets 1",
      "question_type": "NU",
      "original": false,
      "explanations": "Optionnel",
      "video_url": "https://video.com/q1",
      "image_url": "https://image.com/q1",
      "answers": [
        {"text": "Réponse A", "is_correct": true},
        {"text": "Réponse B", "is_correct": false},
        {"text": "Réponse C", "is_correct": false},
        {"text": "Réponse D", "is_correct": false}
      ]
    }
  ],
  "burger_quiz_count": 0
}
```

#### 2.2.3. Création de manche Nuggets

**Endpoint**: `POST /api/quiz/nuggets/`
**Body** :
```json
{
  "title": "Culture générale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

- `title` : obligatoire.  
- `question_ids` : liste d’UUID de questions existantes, ordre = ordre d’affichage.  
- `original` : optionnel (défaut `false`).  

**Contraintes** : nombre de questions **pair** ; toutes les questions doivent avoir `question_type = NU` ; pas de doublon dans `question_ids`.  

**Champs en réponse** : id, title, questions ordonnées, `original`. Champs calculés possibles : `questions_count`, `burger_quiz_count` (ou `used_in_burger_quizzes_count`).

#### 2.2.4. Mise à jour d'une manche Nuggets

**Endpoint** : 
- `PATCH /api/quiz/nuggets/{id}/` pour modifier partiellement (ex. titre, original).  
- `PUT /api/quiz/nuggets/{id}/` pour remplacer complètement la liste de questions.

**Body PATCH** (exemple) :
```json
{
  "title": "Nouveau titre Nuggets",
  "original": true
}
```

**Body PUT** (exemple) :
```json
{
  "title": "Culture générale (v2)",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

**Réponse attendue (200)** : même forme que le détail (cf. 2.2.2), avec les questions complètes.

#### 2.2.5. Suppression d'une manche Nuggets

**Endpoint** : `DELETE /api/quiz/nuggets/{id}/`

- **204 No Content** si la suppression réussit.  
- **404 Not Found** si l’`id` n’existe pas.

---

### 2.3 Manches — Sel ou poivre

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/salt-or-pepper/` | Liste |
| `GET` | `/api/quiz/salt-or-pepper/{id}/` | Détail |
| `POST` | `/api/quiz/salt-or-pepper/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/salt-or-pepper/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/salt-or-pepper/{id}/` | Suppression d’une manche Sel ou poivre |


#### 2.3.1. Liste des manches Sel ou poivre

**Endpoint** : `GET /api/quiz/salt-or-pepper/`

**Réponse attendue** (liste paginée) :
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-sop-1",
      "title": "Noir, Blanc ou Les deux",
      "original": false,
      "questions_count": 2,
      "burger_quiz_count": 0
    }
  ]
}
```

#### 2.3.2. Détail d'une manche Sel ou poivre

**Endpoint** : `GET /api/quiz/salt-or-pepper/{id}/`

En **lecture**, le détail expose les **questions complètes** et leurs réponses, cohérentes avec les propositions :

**Réponse attendue** :
```json
{
  "id": "uuid-sop-1",
  "title": "Noir ou Blanc",
  "original": false,
  "propositions": ["Noir", "Blanc"],
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question 1",
      "question_type": "SP",
      "answers": [
        {"text": "Noir", "is_correct": true},
        {"text": "Blanc", "is_correct": false}
      ]
    }
  ],
  "burger_quiz_count": 0
}
```

#### 2.3.3. Création Sel ou poivre

**Endpoint**: `POST /api/quiz/salt-or-pepper/`
**Body** :
```json
{
  "title": "Noir, Blanc ou Les deux",
  "original": false,
  "description": "Optionnel",
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

- `title` : obligatoire.  
- `propositions` (stocké `choice_labels`) : obligatoire, 2 à 5 libellés, sans doublon.  
- `question_ids` : liste ordonnée d’UUID de questions.  
- `original` : optionnel.  

**Contraintes** : questions de type `SP` ; pour chaque question, les réponses doivent correspondre exactement aux libellés de `propositions`, avec une et une seule réponse correcte.  

**Réponse** : ressource avec `propositions` / `choice_labels`. Champs calculés possibles : `burger_quiz_count`, `questions_count`.

#### 2.3.4. Mise à jour d'une manche Sel ou poivre

**Endpoint** : 
- `PATCH /api/quiz/salt-or-pepper/{id}/` pour modifier, par exemple, le titre.  
- `PUT /api/quiz/salt-or-pepper/{id}/` pour remplacer entièrement la manche.

**Body PATCH** (exemple) :
```json
{
  "title": "Noir, Blanc ou Les deux (v2)"
}
```

**Body PUT** (exemple) :
```json
{
  "title": "Noir, Blanc ou Les deux",
  "original": false,
  "description": "Optionnel",
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

**Réponse attendue (200)** : même forme que le détail (cf. 2.3.2), avec les questions complètes.

#### 2.3.5. Suppression d'une manche Sel ou poivre

**Endpoint** : `DELETE /api/quiz/salt-or-pepper/{id}/`

- **204 No Content** si la suppression réussit.  
- **404 Not Found** si l’`id` n’existe pas.

---

### 2.4 Manches — Menus

#### 2.4.1. Thèmes de menu

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/menu-themes/` | Liste des thèmes |
| `GET` | `/api/quiz/menu-themes/{id}/` | Détail |
| `POST` | `/api/quiz/menu-themes/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/menu-themes/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/menu-themes/{id}/` | Suppression d’un thème de menu |

**POST /api/quiz/menu-themes/** — Corps (exemple) :
```json
{
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "original": true,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

- `type` : `"CL"` (Classique) ou `"TR"` (Troll).  
- `original` : optionnel (défaut **`true`** = créé directement).  
- Questions : type `ME` ; ordre via `question_ids`.  

**Champs calculés** : `questions_count`, `used_in_menus_count`.

**GET /api/quiz/menu-themes/{id}/** — Détail (exemple de réponse) :
```json
{
  "id": "uuid-theme-1",
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "original": true,
  "questions_count": 3,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question Menu 1",
      "question_type": "ME",
      "answers": [
        {"text": "Réponse 1", "is_correct": true}
      ]
    }
  ],
  "used_in_menus_count": 1
}
```

**PUT / PATCH /api/quiz/menu-themes/{id}/** — même corps que le POST, réponse 200 avec le thème complet (comme ci‑dessus).  
**DELETE /api/quiz/menu-themes/{id}/** — 204 No Content en cas de succès.

#### 2.4.2. Manche Menus (regroupe 3 thèmes)

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/menus/` | Liste |
| `GET` | `/api/quiz/menus/{id}/` | Détail |
| `POST` | `/api/quiz/menus/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/menus/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/menus/{id}/` | Suppression d’une manche Menus |

**POST /api/quiz/menus/** — Corps (exemple) :
```json
{
  "title": "Menus du jour",
  "description": "Optionnel",
  "original": false,
  "menu_1_id": "uuid-theme-1",
  "menu_2_id": "uuid-theme-2",
  "menu_troll_id": "uuid-theme-troll"
}
```

**Contraintes** : exactement 2 menus classiques (`menu_1`, `menu_2` avec `type = "CL"`) et 1 menu troll (`menu_troll` avec `type = "TR"`) ; les trois IDs distincts et existants.

**GET /api/quiz/menus/{id}/** — Détail (exemple de réponse) :

En **lecture**, le détail expose les **thèmes complets** avec leurs **questions désérialisées** :

```json
{
  "id": "uuid-menus-1",
  "title": "Menus du jour",
  "description": "Optionnel",
  "original": false,
  "author": {"id": 1, "username": "johndoe"},
  "tags": ["culture"],
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "menu_1": {
    "id": "uuid-theme-1",
    "title": "Cinéma",
    "type": "CL",
    "original": true,
    "author": {"id": 1, "username": "johndoe"},
    "tags": ["cinéma"],
    "questions": [
      {
        "id": "uuid-q1",
        "text": "Qui a réalisé Pulp Fiction ?",
        "question_type": "ME",
        "answers": [{"id": "uuid-a1", "text": "Quentin Tarantino", "is_correct": true}]
      }
    ]
  },
  "menu_2": {
    "id": "uuid-theme-2",
    "title": "Musique",
    "type": "CL",
    "questions": []
  },
  "menu_troll": {
    "id": "uuid-theme-troll",
    "title": "Piège",
    "type": "TR",
    "questions": []
  }
}
```

**PUT / PATCH /api/quiz/menus/{id}/** — même corps que le POST (avec les IDs des thèmes), réponse 200 avec la manche complète incluant les thèmes et questions désérialisées.  
**DELETE /api/quiz/menus/{id}/** — 204 No Content en cas de succès.

---

### 2.5 Manches — Addition

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/additions/` | Liste |
| `GET` | `/api/quiz/additions/{id}/` | Détail |
| `POST` | `/api/quiz/additions/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/additions/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/additions/{id}/` | Suppression d’une manche Addition |

**POST /api/quiz/additions/** — Corps (exemple) :
```json
{
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

**Contraintes** : questions de type `AD` ; pas de doublon dans `question_ids`. Champs calculés possibles : `burger_quiz_count`, `questions_count`.

**GET /api/quiz/additions/{id}/** — Détail (exemple de réponse) :
```json
{
  "id": "uuid-addition-1",
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "questions_count": 3,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question AD 1",
      "question_type": "AD",
      "answers": [
        {"text": "42", "is_correct": true}
      ]
    }
  ],
  "burger_quiz_count": 0
}
```

**PUT / PATCH /api/quiz/additions/{id}/** — même corps que le POST, réponse 200 avec la manche complète (comme ci‑dessus).  
**DELETE /api/quiz/additions/{id}/** — 204 No Content en cas de succès.

---

### 2.6 Manches — Burger de la mort

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/deadly-burgers/` | Liste |
| `GET` | `/api/quiz/deadly-burgers/{id}/` | Détail |
| `POST` | `/api/quiz/deadly-burgers/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/deadly-burgers/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/deadly-burgers/{id}/` | Suppression d’une manche Burger de la mort |

**POST /api/quiz/deadly-burgers/** — Corps (exemple) :
```json
{
  "title": "Burger de la mort - Finale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "…", "uuid-10"]
}
```

**Contraintes** : **10 questions** exactement ; toutes de type `DB`. Champs calculés possibles : `burger_quiz_count`.

**GET /api/quiz/deadly-burgers/{id}/** — Détail (exemple de réponse) :
```json
{
  "id": "uuid-db-1",
  "title": "Burger de la mort - Finale",
  "original": false,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question DB 1",
      "question_type": "DB"
    }
  ],
  "burger_quiz_count": 0
}
```

**PUT / PATCH /api/quiz/deadly-burgers/{id}/** — même corps que le POST, réponse 200 avec la manche complète (comme ci‑dessus).  
**DELETE /api/quiz/deadly-burgers/{id}/** — 204 No Content en cas de succès.

---

### 2.7 Burger Quiz

| Méthode | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quiz/burger-quizzes/` | Liste (avec `created_at`, `updated_at` pour tri/affichage) |
| `GET` | `/api/quiz/burger-quizzes/{id}/` | Détail |
| `POST` | `/api/quiz/burger-quizzes/` | Création |
| `PATCH` \| `PUT` | `/api/quiz/burger-quizzes/{id}/` | Mise à jour |
| `DELETE` | `/api/quiz/burger-quizzes/{id}/` | Suppression d’un Burger Quiz |

**POST /api/quiz/burger-quizzes/** — Corps (exemple) :
```json
{
  "title": "Burger PCaT Episode 1",
  "toss": "Description ou consigne du toss.",
  "nuggets_id": "uuid-nuggets",
  "salt_or_pepper_id": "uuid-sop",
  "menus_id": "uuid-menus",
  "addition_id": "uuid-addition",
  "deadly_burger_id": "uuid-db"
}
```

- `toss` : texte décrivant la manche Toss (à trancher : obligatoire ou optionnel — voir brouillon).  
- IDs des manches : optionnels (null/omis si la manche n’est pas utilisée). Si fournis, doivent référencer des ressources existantes du bon type.  
- Au moins une manche recommandée.  

**Réponse 201** : id, title, toss, `created_at`, `updated_at`, manches liées avec leurs questions complètes.

**GET /api/quiz/burger-quizzes/{id}/** — Détail (exemple de réponse) :

En **lecture**, le détail expose les **manches complètes** avec toutes leurs **questions désérialisées** (intitulé, réponses, métadonnées). Cela permet d'afficher un Burger Quiz complet en une seule requête :

```json
{
  "id": "uuid-bq-1",
  "title": "Burger PCaT Episode 1",
  "toss": "Description ou consigne du toss.",
  "author": {"id": 1, "username": "johndoe"},
  "tags": ["humour", "culture"],
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "nuggets": {
    "id": "uuid-nuggets",
    "title": "Culture générale",
    "original": false,
    "author": {"id": 1, "username": "johndoe"},
    "tags": ["culture"],
    "questions": [
      {
        "id": "uuid-q1",
        "text": "Quelle est la capitale de la France ?",
        "question_type": "NU",
        "original": false,
        "answers": [
          {"id": "uuid-a1", "text": "Paris", "is_correct": true},
          {"id": "uuid-a2", "text": "Lyon", "is_correct": false},
          {"id": "uuid-a3", "text": "Marseille", "is_correct": false},
          {"id": "uuid-a4", "text": "Toulouse", "is_correct": false}
        ]
      }
    ]
  },
  "salt_or_pepper": {
    "id": "uuid-sop",
    "title": "Noir ou Blanc",
    "propositions": ["Noir", "Blanc"],
    "questions": [
      {
        "id": "uuid-q2",
        "text": "La nuit ?",
        "question_type": "SP",
        "answers": [{"id": "uuid-a5", "text": "Noir", "is_correct": true}]
      }
    ]
  },
  "menus": {
    "id": "uuid-menus",
    "title": "Menus du jour",
    "menu_1": {
      "id": "uuid-theme-1",
      "title": "Cinéma",
      "type": "CL",
      "questions": [
        {
          "id": "uuid-q3",
          "text": "Qui a réalisé Pulp Fiction ?",
          "question_type": "ME",
          "answers": [{"id": "uuid-a6", "text": "Quentin Tarantino", "is_correct": true}]
        }
      ]
    },
    "menu_2": {
      "id": "uuid-theme-2",
      "title": "Musique",
      "type": "CL",
      "questions": []
    },
    "menu_troll": {
      "id": "uuid-theme-troll",
      "title": "Piège",
      "type": "TR",
      "questions": []
    }
  },
  "addition": {
    "id": "uuid-addition",
    "title": "Addition rapide",
    "questions": [
      {
        "id": "uuid-q4",
        "text": "2 + 2 ?",
        "question_type": "AD",
        "answers": [{"id": "uuid-a7", "text": "4", "is_correct": true}]
      }
    ]
  },
  "deadly_burger": {
    "id": "uuid-db",
    "title": "Burger de la mort - Finale",
    "questions": [
      {"id": "uuid-q5", "text": "Question DB 1", "question_type": "DB"},
      {"id": "uuid-q6", "text": "Question DB 2", "question_type": "DB"}
    ]
  }
}
```

> **Note** : L'exemple ci-dessus est simplifié. En pratique, chaque manche contient tous ses champs (`created_at`, `updated_at`, `author`, `tags`, etc.) et chaque question contient également ses champs complets (`explanations`, `video_url`, `image_url`, etc.).

**PUT / PATCH /api/quiz/burger-quizzes/{id}/** — même corps que le POST (avec les IDs des manches), réponse 200 avec le Burger Quiz complet incluant les manches et questions désérialisées.  
**DELETE /api/quiz/burger-quizzes/{id}/** — 204 No Content en cas de succès.

---

### 2.8 Récapitulatif Quiz — Contraintes par manche

| Manche | Contrainte |
|--------|------------|
| **Nuggets** | Nombre **pair** de questions ; type `NU`. 4 réponses avec 1 seul correcte |
| **Sel ou poivre** | 2 à 5 propositions ; réponses cohérentes ; type `SP`. |
| **Menus** | 2 menus classiques + 1 menu troll ; questions des thèmes type `ME`. |
| **Addition** | Questions type `AD`. |
| **Burger de la mort** | **10 questions** exactement ; type `DB`. |

---

### 2.9 Champs calculés en lecture seule (listes / détail)

Pour les listes et pages front (Questions, manches, Burger Quiz), l’API peut exposer en lecture seule :

| Ressource | Champ calculé | Description |
|-----------|----------------|-------------|
| **Question** | `usage_count` | Nombre de manches où la question est utilisée. |
| **Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger** | `burger_quiz_count` ou `used_in_burger_quizzes_count` | Nombre de Burger Quiz qui référencent la manche. |
| **Nuggets** | `questions_count` | Nombre de questions (dérivable de la liste). |
| **MenuTheme** | `used_in_menus_count` | Nombre de manches Menus utilisant ce thème. |
| **MenuTheme** | `questions_count` | Nombre de questions du thème. |
| **BurgerQuiz** | — | `created_at` / `updated_at` en base pour tri et affichage. |

---

