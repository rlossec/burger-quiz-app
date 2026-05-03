# Manche Nuggets API

Préfixe : **`/api/quiz/nuggets/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.2 ; contraintes création : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §2.1.

---

## GET /api/quiz/nuggets/

### Description

Liste paginée des manches Nuggets.

### Use cases

- Tableau des manches ; affichage `questions_count`, `burger_quiz_count`

### Permissions

À préciser.

### Response 200

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

---

## GET /api/quiz/nuggets/{id}/

### Description

Détail avec **questions complètes** et réponses (pas seulement les ids).

### Response 200

Voir monolithe §2.2.2 pour l’exemple JSON complet (`questions[]` avec `answers`).

---

## POST /api/quiz/nuggets/

### Description

Crée une manche Nuggets à partir d’ids de questions existantes.

### Use cases

- Assembler une manche après création des questions type `NU`

### Permissions

À préciser.

---

### Body

```json
{
  "title": "Culture générale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

| Champ | Contrainte |
| --- | --- |
| `title` | Obligatoire |
| `question_ids` | UUID existants, ordre = ordre d’affichage |
| `original` | Optionnel, défaut `false` |

---

### Response 201

Ressource Nuggets (id, title, questions ordonnées, `original`, champs calculés éventuels).

---

### Business rules

- Nombre de questions **pair**.
- Toutes les questions : `question_type = NU`.
- Pas de doublon dans `question_ids`.
- Questions existantes.

---

## PATCH /api/quiz/nuggets/{id}/

### Description

Mise à jour partielle (ex. titre, `original`).

### Body (exemple)

```json
{
  "title": "Nouveau titre Nuggets",
  "original": true
}
```

---

## PUT /api/quiz/nuggets/{id}/

### Description

Remplacement complet, notamment la liste `question_ids`.

### Body (exemple)

```json
{
  "title": "Culture générale (v2)",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

### Business rules

- Revalidation des mêmes règles qu’au POST.

---

## DELETE /api/quiz/nuggets/{id}/

### Response

- **204** si succès
- **404** si inconnu
