# Manche Burger de la mort API

Préfixe : **`/api/quiz/deadly-burgers/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.6 ; contraintes : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §2.5.

---

## GET /api/quiz/deadly-burgers/

### Description

Liste paginée des manches Burger de la mort.

### Permissions

À préciser.

---

## GET /api/quiz/deadly-burgers/{id}/

### Description

Détail avec les 10 questions (schéma selon monolithe §2.6).

---

## POST /api/quiz/deadly-burgers/

### Description

Crée une manche avec exactement dix questions.

### Body

```json
{
  "title": "Burger de la mort - Finale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4", "uuid-5", "uuid-6", "uuid-7", "uuid-8", "uuid-9", "uuid-10"]
}
```

---

### Business rules

- **Exactement 10** entrées dans `question_ids`.
- Toutes les questions : `question_type = DB`.
- Pas de doublon ; questions existantes.

---

## PUT / PATCH /api/quiz/deadly-burgers/{id}/

### Description

Mise à jour en conservant la contrainte « 10 questions type DB ».

---

## DELETE /api/quiz/deadly-burgers/{id}/

### Response

**204** si succès.
