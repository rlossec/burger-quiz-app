# API : Endpoints et contraintes de cohérence

Ce document décrit les endpoints prévus pour la création des manches et du Burger Quiz, ainsi que les règles de validation (cohérence) à appliquer avant de persister les données.

---

## 1. Vue d’ensemble du flux

1. **Créer les manches** : Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort.
2. **Créer un Burger Quiz** en fournissant un **toss** et les **IDs des manches** déjà créées.

Les manches sont donc des entités indépendantes ; le Burger Quiz les référence par clé étrangère.

---

## 2. Endpoints de création des manches

### 2.1 Nuggets

**`POST /api/quiz/nuggets/`**

**Corps de la requête (exemple) :**
```json
{
  "title": "Culture générale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

- `title` : chaîne, obligatoire.
- `question_ids` : liste d’UUID de `Question` existantes, dans l’ordre d’affichage. L’ordre dans la liste = ordre de la manche (ou envoyer des paires `{ "question_id": "...", "order": n }` si besoin).
- **`original`** : optionnel (défaut `false`). Champ stocké sur la manche (§2).

**Contraintes métier (validation côté API) :**
- Le **nombre de questions doit être pair** (chaque équipe répond à tour de rôle ; un nombre pair assure l’équité).
- **Type de question** : toutes les questions référencées doivent avoir `question_type = NU` (Nuggets).
- Les questions référencées doivent exister.
- Pas de doublon dans `question_ids`.

**Réponse :** 201 Created + représentation de la ressource Nuggets (id, title, questions ordonnées).

---

### 2.2 Sel ou poivre

Les réponses de chaque question sont **toujours parmi une liste restreinte de propositions** (souvent 2, 3 ou 4 ; maximum 5), définie au niveau de la manche. Exemples : « Noir » / « Blanc », ou « Noir » / « Blanc » / « Les deux ».

**`POST /api/quiz/salt-or-pepper/`**

**Exemple de corps de la requête :**
```json
{
  "title": "Noir, Blanc ou Les deux",
  "original": false,
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

- `title` : obligatoire.
- `description` : optionnel.
- **`propositions`** : **obligatoire**. Liste de 2 à 5 proposition. C’est la liste restreinte parmi laquelle chaque question de la manche doit avoir ses réponses. En base le champ est stocké sous le nom `choice_labels`.
- `question_ids` : liste ordonnée d’UUID de questions.
- `original` : optionnel sur la manche (§2).

**Contraintes métier :**
- **Type de question** : toutes les questions référencées doivent avoir `question_type = SP` (Sel ou Poivre).
- **Propositions** : entre **2 et 5** libellés, sans doublon (string non vide).
- **Cohérence des réponses** : pour chaque question de la manche, le `text` de chaque réponse (Answer) doit être **égal à l’un des libellés** de `propositions` (comparaison stricte ou normalisée selon les besoins). Chaque question doit avoir exactement autant de réponses que de propositions (une par choix), dont **une et une seule** `is_correct = true`.
- Les questions référencées doivent exister.
- Pas de doublon dans `question_ids`.

**Réponse :** 201 Created + ressource SaltOrPepper (avec `propositions` / `choice_labels`).

---

### 2.3 Menus

Une manche **Menus** est composée de **3 thèmes** : deux menus classiques et un menu troll. Chaque thème (`MenuTheme`) a son propre ensemble de questions.

**Création des thèmes de menu (sous-ressources) :**

**`POST /api/quiz/menu-themes/`**
```json
{
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

- `type` : `"CL"` (Classique) ou `"TR"` (Troll).
- Les questions sont ordonnées via `question_ids`. **Type de question** : toutes doivent avoir `question_type = ME` (Menu). (Le champ `original` est sur la manche Menus, pas sur le thème.)

**Création de la manche Menus (regroupe 3 thèmes) :**

**`POST /api/quiz/menus/`**
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

**Contraintes métier :**
- **Exactement 2 menus classiques et 1 menu troll** :
  - `menu_1` et `menu_2` doivent être des `MenuTheme` avec `type = "CL"`.
  - `menu_troll` doit être un `MenuTheme` avec `type = "TR"`.
- Les trois IDs doivent être distincts (pas le même thème deux fois).
- Les thèmes doivent exister.

**Réponse :** 201 Created + ressource Menus (avec les 3 thèmes).

---

### 2.4 Addition

**`POST /api/quiz/additions/`**
```json
{
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

**Contraintes métier :**
- **Type de question** : toutes les questions référencées doivent avoir `question_type = AD` (Addition).
- Les questions doivent exister.
- Pas de doublon dans `question_ids`.
- Règles optionnelles à définir (ex. nombre min/max de questions).

**Réponse :** 201 Created + ressource Addition.

---

### 2.5 Burger de la mort

**`POST /api/quiz/deadly-burgers/`** (ou équivalent)
```json
{
  "title": "Burger de la mort - Finale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", ..., "uuid-10"]
}
```

**Contraintes métier :**
- **Type de question** : toutes les questions référencées doivent avoir `question_type = DB` (Burger de la mort).
- **10 questions** exactement pour cette manche.

---

## 3. Endpoint de création du Burger Quiz

**`POST /api/quiz/burger-quizzes/`**

**Corps de la requête :**
```json
{
  "title": "Session du 15 février 2025",
  "toss": "Description ou consigne du toss.",
  "nuggets_id": "uuid-nuggets",
  "salt_or_pepper_id": "uuid-sop",
  "menus_id": "uuid-menus",
  "addition_id": "uuid-addition",
  "deadly_burger_id": "uuid-db"
}
```

- **`toss`** : texte décrivant la manche Toss. À trancher : obligatoire (cohérence métier) ou optionnel (comme indiqué sur BurgerQuizCreatePage dans la page reference). Documenter le choix dans l’API.
- **IDs des manches** : tous optionnels (null/omis si la manche n’est pas utilisée dans ce quiz). Si fournis, ils doivent référencer des ressources existantes du bon type.

**Contraintes :**
- Au moins une manche devrait être fournie (ou définir une règle métier plus précise).
- Chaque ID doit exister et correspondre au bon modèle (nuggets_id → Nuggets, etc.).

**Réponse :** 201 Created + représentation du Burger Quiz (id, title, toss, **created_at**, **updated_at**, manches liées).

---

## 5. Contraintes sur les questions : type et création par type

### 5.1 Correspondance manche ↔ type de question

Lorsqu’une manche référence des questions, **chaque question doit avoir le `question_type` correspondant** :

| Manche / Ressource | question_type attendu |
|--------------------|------------------------|
| Nuggets            | `NU` |
| SaltOrPepper       | `SP` |
| MenuTheme (Menus)  | `ME` |
| Addition           | `AD` |
| DeadlyBurger       | `DB` |

La validation doit être faite à la création et à la mise à jour des manches (refus si une question a un mauvais type).

### 5.2 Création d’une question : contraintes par type

Lors de la **création (ou mise à jour) d’une Question** via l’API, les contraintes suivantes doivent être respectées selon `question_type` :

| Type | Code | Contraintes sur les réponses (Answer) |
|------|------|----------------------------------------|
| **Nuggets**      | `NU` | Exactement **4 réponses**, dont **une et une seule** `is_correct = true`. |
| **Sel ou poivre**| `SP` | Exactement **2 réponses** (les deux choix de la manche), dont **une** `is_correct = true`. |
| **Menu**         | `ME` | À définir (ex. 4 réponses comme Nuggets, ou autre règle). |
| **Addition**     | `AD` | À définir (ex. 4 réponses, 1 correcte). |
| **Burger de la mort** | `DB` | À définir (ex. 1 seule réponse correcte, pas de QCM ?). |

L’endpoint de création de questions (ex. `POST /api/quiz/questions/`) devra valider ces règles en fonction de `question_type` et des `answers` envoyées (ou créées avec la question). Il devra aussi accepter :
- le champ **`original`** (booléen) sur la Question (§2) ;
- les champs optionnels **`video_url`** et **`audio_url`** (§2.5).

---

## 6. Récapitulatif des contraintes de cohérence (manches)

| Manche           | Contrainte |
|------------------|------------|
| **Nuggets**      | Nombre **pair** de questions ; questions de type `NU`. |
| **Sel ou poivre**| Nombre **fini** de propositions : toutes les questions ont les mêmes 2 choix ; questions de type `SP`. |
| **Menus**        | Exactement **2 menus classiques** (menu_1, menu_2) et **1 menu troll** (menu_troll) ; questions des thèmes de type `ME`. |
| **Addition**     | Questions de type `AD` ; autres règles optionnelles. |
| **Burger de la mort** | **10 questions** exactement ; questions de type `DB`. |

---

## 7. Endpoints complémentaires utiles

- **GET** sur chaque type de manche : liste et détail (ex. `GET /api/quiz/nuggets/`, `GET /api/quiz/nuggets/<id>/`). En réponse, la manche expose son champ **`original`** (stocké en base). Le champ est accepté en création/mise à jour (POST/PATCH).
- **GET** sur les questions : liste/détail avec filtrage par **`?original=true|false`** et **`?question_type=NU|SP|ME|AD|DB`**.
- **PATCH / PUT** pour modifier une manche (en re-vérifiant les contraintes, dont le type des questions).
- **GET** Burger Quiz : liste et détail (avec `created_at`, `updated_at` pour tri et affichage « date/création »).
- **GET** questions/answers : pour construire les payloads (liste de questions par type, etc.).

Le détail (paramètres de filtre, pagination, schémas de réponse) est décrit dans **`docs/api-reference.md`** (sections Burger Quiz et Accounts).

### 7.1 Champs calculés en lecture seule (pour les listes front)

Pour alimenter les tableaux des pages (QuestionsListPage, NuggetsListPage, SaltOrPepperListPage, MenuListPage, MenuThemeListPage, AdditionListPage, DeadlyBurgerListPage, BurgerQuizListPage), l’API peut exposer les champs calculés suivants **en lecture seule** (sans les stocker en base) :

| Ressource | Champ calculé | Description |
|-----------|----------------|--------------|
| **Question** (liste/détail) | `usage_count` | Nombre de manches où la question est utilisée (NuggetQuestion + DeadlyBurgerQuestion + 0 ou 1 pour SP/ME/AD). Permet d’afficher « nombre d’utilisations » sur QuestionsListPage. |
| **Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger** (liste/détail) | `burger_quiz_count` ou `used_in_burger_quizzes_count` | Nombre de BurgerQuiz qui référencent cette manche. Permet d’afficher « nombre d’utilisation » sur les listes de manches. |
| **Nuggets** (liste/détail) | — | « Nombre de Nuggets » affiché = nombre de questions de la manche ; peut être dérivé de la liste des questions ou exposé comme `questions_count`. |
| **MenuTheme** (liste/détail) | `used_in_menus_count` | Nombre de manches Menus qui utilisent ce thème (en menu_1, menu_2 ou menu_troll). |
| **MenuTheme** (liste/détail) | `questions_count` | Nombre de questions du thème. |
| **BurgerQuiz** (liste) | — | `created_at` / `updated_at` en base pour « date/création » et tri. |

---

## 8. Cheminement pour créer un Burger Quiz entier

Ordre recommandé des appels API pour constituer un quiz complet :

1. **Questions et réponses**
   - Créer les **Questions** avec `question_type`, **`original`** (booléen), **Answers** conformes aux contraintes du type, et optionnellement **`video_url`** / **`audio_url`**.
   - Pour les types SP, ME, AD : créer les questions en les associant à la manche concernée (chaque question n’appartient qu’à une seule manche). Pour NU et DB, les questions peuvent être créées puis réutilisées dans plusieurs manches.
   - Endpoint(s) : `POST /api/quiz/questions/` (et réponses associées selon le design retenu).

2. **Manches**
   - **Nuggets** : `POST /api/quiz/nuggets/` avec `title`, `question_ids` (nombre pair, questions type `NU`).
   - **Sel ou poivre** : `POST /api/quiz/salt-or-pepper/` avec `title`, `question_ids` (questions type `SP`, mêmes 2 choix pour toutes).
   - **Menus** :
     - Créer 3 **MenuTheme** : `POST /api/quiz/menu-themes/` (2 avec `type = "CL"`, 1 avec `type = "TR"`), chacun avec ses `question_ids` (type `ME`).
     - Puis `POST /api/quiz/menus/` avec `menu_1_id`, `menu_2_id`, `menu_troll_id`.
   - **Addition** : `POST /api/quiz/additions/` avec `title`, `question_ids` (questions type `AD`).
   - **Burger de la mort** (optionnel) : `POST /api/quiz/deadly-burgers/` avec `title`, `question_ids` (10 questions type `DB`).

3. **Burger Quiz**
   - `POST /api/quiz/burger-quizzes/` avec `title`, **toss** (obligatoire), et les IDs des manches créées : `nuggets_id`, `salt_or_pepper_id`, `menus_id`, `addition_id`, `deadly_burger_id` (tous optionnels mais au moins une manche recommandée).

Aucune implémentation ne sera engagée avant votre validation de ces endpoints et contraintes.
