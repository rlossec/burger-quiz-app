# Accounts — JWT (SimpleJWT)

Préfixe : **`/api/auth/jwt/`**

Index : [`README.md`](README.md)

---

## POST /api/auth/jwt/create/

### Description

Émet un couple access / refresh à partir de `username` et `password`.

### Use cases

- Connexion applicative ; en-tête `Authorization: Bearer <access>` pour la suite.

### Permissions

Public (identifiants valides requis).

---

### Body

```json
{
  "username": "string",
  "password": "string"
}
```

| Champ | Contrainte |
| --- | --- |
| `username` | Obligatoire |
| `password` | Obligatoire |

---

### Response 200

```json
{
  "access": "string",
  "refresh": "string"
}
```

---

### Business rules

- Utiliser `access` dans `Authorization: Bearer <access>` pour les requêtes authentifiées.

---

## POST /api/auth/jwt/refresh/

### Description

Rafraîchit l’access token (et éventuellement le refresh selon config).

### Permissions

Public (refresh valide requis).

### Body

```json
{
  "refresh": "string"
}
```

### Response 200

```json
{
  "access": "string",
  "refresh": "string"
}
```

---

## POST /api/auth/jwt/verify/

### Description

Vérifie la validité d’un token.

### Body

```json
{
  "token": "string"
}
```

### Response 200

`{}` si le token est valide.
