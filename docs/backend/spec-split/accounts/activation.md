# Accounts — Activation de compte

Index : [`README.md`](README.md)

Flux **post-inscription** : valider l’email via uid + token, ou renvoyer le message d’activation.

Corps et codes de réponse exacts : **documentation Djoser** + cas dans [`docs/tests/accounts.md`](../../../tests/accounts.md).

---

## POST /api/auth/users/activation/

### Description

Active un compte à partir du lien reçu par email (typiquement `uid` + `token`).

### Use cases

- Finaliser l’inscription lorsque l’activation par email est activée.

### Permissions

Public (les jetons portent la sécurité).

---

### Body

Voir Djoser (`uid`, `token`, etc. selon version).

---

### Business rules

- Jetons à usage limité / expiration selon configuration.

---

## POST /api/auth/users/resend_activation/

### Description

Renvoie l’email d’activation (ex. si le premier a expiré).

### Permissions

Public ou authentifié selon configuration Djoser.

---

### Body

Voir Djoser (souvent email de l’utilisateur).
