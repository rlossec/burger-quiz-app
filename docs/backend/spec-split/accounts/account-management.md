# Accounts — Inscription et gestion du compte (`me`)

Index : [`README.md`](README.md)

Inscription publique (`POST /users/`) et opérations sur la ressource **`/users/me/`** (utilisateur authentifié), exposées par le `UserViewSet` Djoser (méthodes usuelles sur `me` : **GET**, **PUT**, **PATCH**, **DELETE**).

---

## POST /api/auth/users/

### Description

Inscription (création de compte).

### Use cases

- Créer un utilisateur ; compte souvent inactif jusqu’à activation par email.

### Permissions

Public (selon configuration Djoser).

---

### Body

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securePassword123",
  "re_password": "securePassword123"
}
```

| Champ | Contrainte |
| --- | --- |
| `email` | Obligatoire, unique, format email valide |
| `username` | Obligatoire, unique, max 150 car., caractères Django user |
| `password` | Obligatoire (règles Django) |
| `re_password` | Obligatoire, identique à `password` |

---

### Response 201

Représentation utilisateur (serializer projet, sans mot de passe).

---

### Business rules

- Compte possiblement inactif jusqu’à [`activation.md`](activation.md).

---

## GET /api/auth/users/me/

### Description

Utilisateur actuellement authentifié.

### Permissions

Authentifié (JWT).

### Response 200

Même schéma que le détail utilisateur (cf. [`users.md`](users.md) / monolithe §1.2).

---

## PUT /api/auth/users/me/

### Description

Mise à jour **complète** du profil connecté (même logique qu’un `PUT` sur la ressource utilisateur « soi »).

### Permissions

Authentifié.

### Body / champs

Typiquement : `email`, `first_name`, `last_name`, `avatar` ; `id` et `username` en lecture seule (cf. monolithe §1.2).

---

### Business rules

- Changement d’`email` peut désactiver le compte jusqu’à confirmation selon règles projet.

---

## PATCH /api/auth/users/me/

### Description

Mise à jour **partielle** du profil connecté (dont avatar).

### Permissions

Authentifié.

### Body

Champs modifiables typiques : `email`, `first_name`, `last_name`, `avatar`. `id` et `username` en lecture seule (cf. monolithe).

---

### Business rules

- Changement d’`email` peut désactiver le compte jusqu’à confirmation selon règles projet.

---

## DELETE /api/auth/users/me/

### Description

Suppression du **compte de l’utilisateur connecté** (sans passer par `users/{id}/`).

### Permissions

Authentifié.

### Response

Selon Djoser / projet (ex. **204** No Content).

---

### Business rules

- Équivalent métier à la suppression du compte courant ; vérifier la cohérence avec `DELETE /users/{id}/` lorsque `id` est celui de l’utilisateur connecté (cf. [`users.md`](users.md)).
