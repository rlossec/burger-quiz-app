# Accounts — index API

Préfixe : **`/api/auth/`** (Djoser + SimpleJWT).

Source monolithe : [`../../api-specifications.md`](../../api-specifications.md) §1.

Modèle de structure : [`../../../module-endpoints-index-template.md`](../../../module-endpoints-index-template.md).

---

## Fichiers par groupe

| Fichier | Périmètre |
| --- | --- |
| [`jwt.md`](jwt.md) | Tokens JWT (create, refresh, verify) |
| [`account-management.md`](account-management.md) | Inscription + `users/me/` (GET, PUT, PATCH, DELETE) |
| [`users.md`](users.md) | Liste `users/` + cycle de vie `users/{id}/` (droits self vs staff) |
| [`activation.md`](activation.md) | Activation de compte et renvoi d’email |
| [`reset.md`](reset.md) | Réinitialisation mot de passe et nom d’utilisateur (Djoser) |

---

## Endpoints — récapitulatif

| Méthode | Chemin | Description | Documentation |
| --- | --- | --- | --- |
| `POST` | `/api/auth/jwt/create/` | Obtenir access + refresh | [`jwt.md`](jwt.md) |
| `POST` | `/api/auth/jwt/refresh/` | Rafraîchir les tokens | [`jwt.md`](jwt.md) |
| `POST` | `/api/auth/jwt/verify/` | Vérifier un token | [`jwt.md`](jwt.md) |
| `POST` | `/api/auth/users/` | Inscription | [`account-management.md`](account-management.md) |
| `GET` | `/api/auth/users/me/` | Profil utilisateur connecté | [`account-management.md`](account-management.md) |
| `PUT` | `/api/auth/users/me/` | Mise à jour complète du profil (self) | [`account-management.md`](account-management.md) |
| `PATCH` | `/api/auth/users/me/` | Mise à jour partielle du profil (self) | [`account-management.md`](account-management.md) |
| `DELETE` | `/api/auth/users/me/` | Suppression du compte connecté | [`account-management.md`](account-management.md) |
| `GET` | `/api/auth/users/` | Liste des utilisateurs | [`users.md`](users.md) |
| `GET` | `/api/auth/users/{id}/` | Détail utilisateur | [`users.md`](users.md) |
| `PUT` | `/api/auth/users/{id}/` | Mise à jour complète (propriétaire) | [`users.md`](users.md) |
| `PATCH` | `/api/auth/users/{id}/` | Mise à jour partielle (propriétaire) | [`users.md`](users.md) |
| `DELETE` | `/api/auth/users/{id}/` | Suppression de compte | [`users.md`](users.md) |
| `POST` | `/api/auth/users/activation/` | Activer un compte (uid + token) | [`activation.md`](activation.md) |
| `POST` | `/api/auth/users/resend_activation/` | Renvoyer l’email d’activation | [`activation.md`](activation.md) |
| `POST` | `/api/auth/users/reset_password/` | Demande reset mot de passe | [`reset.md`](reset.md) |
| `POST` | `/api/auth/users/reset_password_confirm/` | Confirmer nouveau mot de passe | [`reset.md`](reset.md) |
| `POST` | `/api/auth/users/reset_username/` | Demande reset nom d’utilisateur | [`reset.md`](reset.md) |
| `POST` | `/api/auth/users/reset_username_confirm/` | Confirmer nouveau nom d’utilisateur | [`reset.md`](reset.md) |

Schémas Djoser détaillés et jeux de tests : documentation Djoser + [`docs/tests/accounts.md`](../../../tests/accounts.md) si présent.
