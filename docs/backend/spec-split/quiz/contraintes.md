# Quiz : contraintes, flux et récapitulatifs

Index : [`README.md`](README.md)

Les fiches endpoints : `questions.md`, `nuggets.md`, `salt-or-pepper.md`, `menus.md`, `additions.md`, `deadly-burger.md`, `quizzes.md` (même dossier).

---

## 1. Vue d’ensemble du flux

1. Créer les **manches** : Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort.
2. Créer un **Burger Quiz** en fournissant un **toss** et les **ids** des manches déjà persistées.

Les manches sont des entités indépendantes ; le Burger Quiz les référence par clé étrangère.

---

## 2. Endpoints de création des manches (rappel)

| Manche | Méthode | Chemin |
| --- | --- | --- |
| Nuggets | `POST` | `/api/quiz/nuggets/` |
| Sel ou poivre | `POST` | `/api/quiz/salt-or-pepper/` |
| Thème menu | `POST` | `/api/quiz/menu-themes/` |
| Menus (3 thèmes) | `POST` | `/api/quiz/menus/` |
| Addition | `POST` | `/api/quiz/additions/` |
| Burger de la mort | `POST` | `/api/quiz/deadly-burgers/` |

---

## 3. Création du Burger Quiz

**`POST /api/quiz/burger-quizzes/`**

- Champs : `title`, `toss`, `nuggets_id`, `salt_or_pepper_id`, `menus_id`, `addition_id`, `deadly_burger_id`.
- `toss` : obligation à trancher (cohérence métier vs optionnel front).
- Ids de manches : optionnels si manche non utilisée ; si fournis → existants et **bon type**.

**Contraintes**

- Au moins une manche devrait être fournie (ou règle plus précise à figer).

Fiche endpoint : [`quizzes.md`](quizzes.md).

---

## 4. Correspondance manche ↔ `question_type`

Lorsqu’une manche référence des questions, chaque question doit avoir le type attendu :

| Manche / ressource | `question_type` |
| --- | --- |
| Nuggets | `NU` |
| SaltOrPepper | `SP` |
| MenuTheme (Menus) | `ME` |
| Addition | `AD` |
| DeadlyBurger | `DB` |

Validation à la création et à la mise à jour des manches.

---

## 5. Création / mise à jour d’une question : contraintes par type

| Type | Code | Contraintes sur les réponses |
| --- | --- | --- |
| Nuggets | `NU` | **4** réponses, **une seule** `is_correct = true` |
| Sel ou poivre | `SP` | **2** réponses, **une** correcte (alignées sur les propositions de la manche en contexte SP) |
| Menu | `ME` | À définir (ex. 4 réponses / autre) |
| Addition | `AD` | À définir (ex. 4 réponses, 1 correcte) |
| Burger de la mort | `DB` | À définir |

Champs à prendre en charge côté API : `original` (bool), `video_url`, `audio_url` (optionnels) — cf. monolithe.

---

## 6. Récapitulatif contraintes de cohérence (manches)

| Manche | Contrainte |
| --- | --- |
| Nuggets | Nombre **pair** de questions ; type `NU` |
| Sel ou poivre | 2 à 5 propositions ; cohérence des réponses avec les libellés ; type `SP` |
| Menus | 2 thèmes `CL` + 1 thème `TR` ; questions des thèmes type `ME` |
| Addition | Type `AD` ; autres règles optionnelles |
| Burger de la mort | **10** questions ; type `DB` |

---

## 7. Endpoints complémentaires et champs calculés

- **GET** listes / détails sur chaque type de manche et sur les questions (filtres `original`, `question_type`).
- **PATCH / PUT** manches : revalidation des contraintes.
- **GET** Burger Quiz : liste / détail avec timestamps.

### Champs calculés (listes front)

| Ressource | Champ | Rôle |
| --- | --- | --- |
| Question | `usage_count` | Nb de manches utilisant la question |
| Manches (Nuggets, SP, Menus, Addition, DB) | `burger_quiz_count` ou équivalent | Nb de Burger Quiz référençant la manche |
| MenuTheme | `used_in_menus_count`, `questions_count` | Usage et taille du thème |
| BurgerQuiz | `created_at`, `updated_at` | Tri / affichage date |

Référence croisée : le monolithe §7 cite `docs/api-reference.md` (fichier non présent à ce chemin dans le dépôt actuel) ; schémas détaillés : [`../../api-specifications.md`](../../api-specifications.md).

---

## 8. Cheminement pour créer un Burger Quiz entier

Ordre recommandé des appels :

1. **Questions** — `POST /api/quiz/questions/` avec types et réponses conformes §5.
2. **Manches** — dans l’ordre métier souhaité : Nuggets → Sel ou poivre → MenuThemes + Menus → Addition → Deadly burger (si utilisé).
3. **Burger Quiz** — `POST /api/quiz/burger-quizzes/` avec `title`, `toss`, ids des manches.
