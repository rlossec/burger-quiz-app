# Burger Quiz API

Préfixe : **`/api/quiz/burger-quizzes/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.7 ; contraintes agrégées : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §3.

---

## GET /api/quiz/burger-quizzes/

### Description

Liste des Burger Quiz avec `created_at` / `updated_at` pour tri et affichage.

### Use cases

- Page liste des sessions quiz

### Permissions

À préciser.

---

## GET /api/quiz/burger-quizzes/{id}/

### Description

Détail avec références aux manches (aperçu titre + id).

### Response 200

Voir monolithe §2.7 (objets `nuggets`, `salt_or_pepper`, `menus`, `addition`, `deadly_burger`, timestamps).

---

## POST /api/quiz/burger-quizzes/

### Description

Assemble un Burger Quiz à partir des manches déjà créées.

### Body

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

| Champ | Contrainte |
| --- | --- |
| `title` | Selon règles produit |
| `toss` | À trancher : obligatoire vs optionnel (cf. monolithe + page référence front) |
| `*_id` | Optionnels / null si manche non utilisée ; si présents → ressource existante du **bon** type |

---

### Business rules

- Au moins une manche **recommandée** (règle métier à figer).
- Chaque id doit exister et correspondre au modèle attendu (Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger).

---

### Response 201

`id`, `title`, `toss`, `created_at`, `updated_at`, manches liées (forme détail).

---

## PUT / PATCH /api/quiz/burger-quizzes/{id}/

### Description

Mise à jour du quiz (même corps que POST, réponse 200 complète).

---

## DELETE /api/quiz/burger-quizzes/{id}/

### Response

**204** si succès.
