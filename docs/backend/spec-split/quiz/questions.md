# Questions Quiz API

Préfixe : **`/api/quiz/questions/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.1 ; contraintes par type : [`contraintes.md`](contraintes.md).

---

## GET /api/quiz/questions/

### Description

Liste paginée des questions avec filtres.

### Use cases

- Liste admin / éditorial
- Filtrer par `original` ou `question_type` pour composer les manches

### Permissions

À préciser côté implémentation (typiquement authentifié + rôle éditeur).

---

### Query params

| Param | Type | Description |
| --- | --- | --- |
| `original` | bool | `true` \| `false` |
| `question_type` | string | `NU` \| `SP` \| `ME` \| `AD` \| `DB` |

---

### Response 200

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "text": "intitulé",
      "question_type": "NU",
      "original": false,
      "explanations": "…",
      "video_url": "https://…",
      "image_url": "https://…",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    }
  ]
}
```

Champs calculés optionnels : voir vue d’ensemble (`usage_count`).

---

## GET /api/quiz/questions/{id}/

### Description

Détail d’une question avec ses réponses.

### Permissions

À préciser.

### Response 200

```json
{
  "id": "uuid",
  "text": "…",
  "question_type": "NU",
  "original": true,
  "explanations": "…",
  "video_url": "https://…",
  "image_url": "https://…",
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "answers": [
    {"text": "Paris", "is_correct": true},
    {"text": "Lyon", "is_correct": false}
  ]
}
```

---

## POST /api/quiz/questions/

### Description

Crée une question et ses réponses selon `question_type`.

### Use cases

- Alimenter le catalogue avant création des manches

### Permissions

À préciser.

---

### Body

```json
{
  "text": "intitulé de la question",
  "question_type": "NU",
  "answers": [
    {"text": "Paris", "is_correct": true},
    {"text": "Lyon", "is_correct": false}
  ],
  "video_url": "https://…",
  "audio_url": "https://…",
  "original": false
}
```

---

### Business rules

- Contraintes sur `answers` selon `question_type` : voir [`contraintes.md`](contraintes.md) § « Création / mise à jour d’une question ».

---

## PUT /api/quiz/questions/{id}/

### Description

Remplacement complet (idempotent).

### Body

Même forme qu’au POST (ressource complète).

### Response 200

Même forme que le détail GET.

---

## PATCH /api/quiz/questions/{id}/

### Description

Mise à jour partielle.

### Body (exemple)

```json
{
  "text": "Libellé corrigé",
  "original": false
}
```

### Response 200

Ressource complète question (forme détail).

---

## DELETE /api/quiz/questions/{id}/

### Description

Supprime la question.

### Response

- **204** si succès
- **404** si id inconnu
