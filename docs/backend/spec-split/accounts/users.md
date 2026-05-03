# Accounts — Liste et utilisateurs par id

Index : [`README.md`](README.md)

Ce groupe regroupe la **liste** des utilisateurs (rôle élevé) et les opérations sur **`/users/{id}/`**, y compris lorsque l’utilisateur agit sur **son propre** id (détail / mise à jour / suppression). La distinction se fait par **permissions**, pas par URL.

---

## GET /api/auth/users/

### Description

Liste paginée des utilisateurs.

### Use cases

- Back-office, support (staff / superuser).

### Permissions

Authentifié ; **staff ou superuser** pour la liste complète (cf. monolithe).

---

### Query params

Pagination : `page`, `page_size` (ex. 10 par page selon spec actuelle).

---

### Response 200

Liste paginée : champs typiques `id`, `email`, `username`, `first_name`, `last_name`, `avatar`.

---

## GET /api/auth/users/{id}/

### Description

Détail d’un utilisateur.

### Permissions

Authentifié. Utilisateur standard : **uniquement son** `id`. Staff / superuser : tout `id`.

---

### Response 200

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

---

## PUT /api/auth/users/{id}/

### Description

Mise à jour **complète** du compte.

### Permissions

**Propriétaire** du compte (`id` = utilisateur connecté).

---

### Body / champs

Comme monolithe : `email`, `first_name`, `last_name`, `avatar` ; `id` et `username` en lecture seule.

---

### Business rules

- Changement d’email peut exiger reconfirmation.

---

## PATCH /api/auth/users/{id}/

### Description

Mise à jour **partielle** (mêmes règles que PUT, champs partiels).

### Permissions

Propriétaire du compte.

---

## DELETE /api/auth/users/{id}/

### Description

Suppression du compte.

### Permissions

Propriétaire ou **staff** selon règles métier (cf. tests [`docs/tests/accounts.md`](../../../tests/accounts.md)).

### Response

Selon implémentation Djoser / projet (204 ou message).
