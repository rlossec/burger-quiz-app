# Accounts — Réinitialisation (mot de passe et nom d’utilisateur)

Index : [`README.md`](README.md)

Djoser expose **deux flux parallèles** : mot de passe et nom d’utilisateur. Chacun suit le même schéma **demande** (email) → **confirmation** (`uid`, `token`, nouvelle valeur). Deux sections thématiques dans ce fichier.

Référence schémas : documentation Djoser + [`docs/tests/accounts.md`](../../../tests/accounts.md).

---

## Reset Mot de passe

### POST /api/auth/users/reset_password/

#### Description

Demande de réinitialisation : envoi d’un email avec lien / token.

#### Permissions

Public.

#### Body

Email (ou identifiant attendu par Djoser).

---

### POST /api/auth/users/reset_password_confirm/

#### Description

Confirmation : définit le nouveau mot de passe à partir de `uid`, `token`, `new_password` (noms exacts selon Djoser).

#### Permissions

Public : uid et token dans l'url envoyé.

---

### Business rules (mot de passe)

- Ne pas exposer si l’email existe ou non (énumération) selon bonnes pratiques sécurité.

## Reset Nom d’utilisateur

### POST /api/auth/users/reset_username/

#### Description

Demande de réinitialisation du **username** via email.

#### Permissions

Public.

---

### POST /api/auth/users/reset_username_confirm/

#### Description

Confirmation avec `uid`, `token`, `new_username` (selon Djoser).

#### Permissions

Public (jeton requis).

---

### Business rules (nom d’utilisateur)

- Aligner les règles de `username` sur celles de l’inscription (unicité, caractères autorisés).
