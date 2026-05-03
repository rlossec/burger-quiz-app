# Manche Addition API

Préfixe : **`/api/quiz/additions/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.5 ; contraintes : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §2.4.

---

## GET /api/quiz/additions/

### Description

Liste paginée des manches Addition.

### Permissions

À préciser.

---

## GET /api/quiz/additions/{id}/

### Description

Détail avec questions type `AD` complètes.

### Response 200

Voir monolithe §2.5 (exemple avec `questions_count`, `burger_quiz_count`).

---

## POST /api/quiz/additions/

### Description

Crée une manche Addition.

### Body

```json
{
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

---

### Business rules

- Toutes les questions : `question_type = AD`.
- Questions existantes ; pas de doublon dans `question_ids`.
- Règles min/max de nombre de questions : optionnelles / à trancher (cf. monolithe contraintes).

---

## PUT / PATCH /api/quiz/additions/{id}/

### Description

Mise à jour ; réponse 200 = manche complète.

### Business rules

- Revalidation côté API (types, doublons).

---

## DELETE /api/quiz/additions/{id}/

### Response

**204** si succès.
