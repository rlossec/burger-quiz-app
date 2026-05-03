# Référence API Burger Quiz

### Base URL et versions :

**Base URL**: `/api/`

Pas de versions différentes

### Format

- JSON
- Dates : ISO 8601 UTC (ex. `2025-01-01T12:00:00Z`)
- Identifiants : UUID RFC 4122 là où le monolithe les utilise

## 1. Authentification

### Méthode

JWT Bearer.

En-tête : `Authorization: Bearer <access_token>`

Obtenir un couple de tokens : `POST /api/auth/jwt/create/`.

### Codes d’erreur globaux liés à l’auth

| Code | Signification |
| --- | --- |
| 401 | Token absent ou invalide |
| 403 | Permission insuffisante |

---

## 2. Format des réponses

### Liste paginée (schéma courant)

```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": []
}
```

Paramètres usuels (selon vue DRF) : `page`, `page_size`, `ordering`, `search` / filtres dédiés par ressource.

### Succès (ressource)

Voir les fiches endpoints pour les champs par type (`Question`, manches, `BurgerQuiz`, etc.).

## 3. Format des erreurs (global)

Documenter les erreurs métier une fois par domaine ; formats types :

### 3.1 Validation — 400

```json
{
  "field_name": ["Message d’erreur"]
}
```

### 3.2 Erreur métier — 400

```json
{
  "detail": "Message métier"
}
```

### 3.3 Non trouvé — 404

```json
{
  "detail": "Not found."
}
```

## 4. Permissions

Accounts : comportement Djoser + SimpleJWT — voir [`accounts/README.md`](accounts/README.md).

Quiz : manches, questions, Burger Quiz — voir [`quiz/README.md`](quiz/README.md).

| Rôle | Capacités (indicatif) |
| --- | --- |
| Public | Selon endpoints exposés sans auth |
| Authenticated | Profil, ressources « self » |
| Staff / superuser | Liste utilisateurs, administration quiz |

## 5. Ressources — index des specs détaillées

| Domaine | Préfixe | Spec détaillée (pilote) |
| --- | --- | --- |
| Accounts | `/api/auth/` | [`accounts/README.md`](accounts/README.md) |
| Quiz | `/api/quiz/` | [`quiz/README.md`](quiz/README.md) |

