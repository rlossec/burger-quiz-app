# Manche Sel ou poivre API

Préfixe : **`/api/quiz/salt-or-pepper/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.3 ; contraintes : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §2.2.

---

## GET /api/quiz/salt-or-pepper/

### Description

Liste paginée des manches Sel ou poivre.

### Use cases

- Listes front ; compteurs `questions_count`, `burger_quiz_count`

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
      "id": "uuid-sop-1",
      "title": "Noir, Blanc ou Les deux",
      "original": false,
      "questions_count": 2,
      "burger_quiz_count": 0
    }
  ]
}
```

---

## GET /api/quiz/salt-or-pepper/{id}/

### Description

Détail avec questions complètes et `propositions` (alias stockage `choice_labels`).

### Response 200

Voir monolithe §2.3.2.

---

## POST /api/quiz/salt-or-pepper/

### Description

Crée une manche avec liste restreinte de propositions partagées par toutes les questions.

### Permissions

À préciser.

---

### Body

```json
{
  "title": "Noir, Blanc ou Les deux",
  "original": false,
  "description": "Optionnel",
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

| Champ | Contrainte |
| --- | --- |
| `title` | Obligatoire |
| `propositions` | Obligatoire, 2 à 5 libellés non vides, sans doublon |
| `question_ids` | Ordre d’affichage |
| `original` | Optionnel |

---

### Business rules

- Toutes les questions : `question_type = SP`.
- Pour chaque question, chaque `Answer.text` doit être **l’un des** libellés de `propositions`.
- Une et une seule réponse correcte par question.
- Pas de doublon dans `question_ids`.

---

## PATCH /api/quiz/salt-or-pepper/{id}/

### Description

Mise à jour partielle (ex. titre).

---

## PUT /api/quiz/salt-or-pepper/{id}/

### Description

Remplacement complet de la manche (titre, propositions, questions).

### Business rules

- Mêmes contraintes qu’au POST.

---

## DELETE /api/quiz/salt-or-pepper/{id}/

### Response

- **204** / **404**
