# Menus API (thèmes + manche)

Préfixes : **`/api/quiz/menu-themes/`** et **`/api/quiz/menus/`**

Index : [`README.md`](README.md)

Source : [`../../api-specifications.md`](../../api-specifications.md) §2.4 ; contraintes : [`../../api-endpoints-et-contraintes.md`](../../api-endpoints-et-contraintes.md) §2.3.

---

## GET /api/quiz/menu-themes/

### Description

Liste des thèmes de menu.

### Use cases

- Préparer les trois thèmes avant `POST /menus/`

### Permissions

À préciser.

---

## GET /api/quiz/menu-themes/{id}/

### Description

Détail d’un thème avec questions type `ME` et champs calculés (`questions_count`, `used_in_menus_count`).

### Response 200

Voir monolithe §2.4.1.

---

## POST /api/quiz/menu-themes/

### Description

Crée un thème (classique ou troll) et attache des questions.

### Body

```json
{
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

| Champ | Contrainte |
| --- | --- |
| `type` | `"CL"` (classique) ou `"TR"` (troll) |
| `question_ids` | Toutes les questions : `question_type = ME` |

---

### Business rules

- Ordre des questions = ordre de `question_ids`.
- Le champ `original` est porté par la manche Menus, pas par le thème (cf. monolithe).

---

## PUT / PATCH /api/quiz/menu-themes/{id}/

### Description

Mise à jour complète ou partielle ; réponse 200 avec thème complet.

---

## DELETE /api/quiz/menu-themes/{id}/

### Response

**204** si succès.

---

## GET /api/quiz/menus/

### Description

Liste des manches Menus (regroupement de 3 thèmes).

---

## GET /api/quiz/menus/{id}/

### Description

Détail avec `menu_1`, `menu_2`, `menu_troll` (objets ou ids selon implémentation — voir monolithe §2.4.2).

---

## POST /api/quiz/menus/

### Description

Crée la manche Menus à partir de trois `MenuTheme` existants.

### Body

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

---

### Business rules

- `menu_1` et `menu_2` : thèmes avec `type = CL`.
- `menu_troll` : thème avec `type = TR`.
- Les trois UUID distincts et existants.

---

## PUT / PATCH / DELETE /api/quiz/menus/{id}/

### Description

Mise à jour ou suppression ; **204** sur DELETE si succès.

### Business rules (PUT/PATCH)

- Revalidation des règles du POST.
