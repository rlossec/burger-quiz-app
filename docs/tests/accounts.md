# Tests du module Accounts

Ce document décrit les tests unitaires et d'intégration du module `accounts` (authentification et gestion des utilisateurs).

## Exécution des tests

Pour exécuter tous les tests du module accounts

```bash
python manage.py test accounts.tests
```
et Avec Docker
```bash
docker compose exec backend uv run python manage.py test accounts.tests
```


## Structure des tests

| Fichier | Classes | Couverture |
|---------|---------|------------|
| `test_activation.py` | `TestActivationEndpoints` | Activation de compte, renvoi d'email |
| `test_jwt.py` | `TestJWTEndpoints` | Création, rafraîchissement et vérification des tokens JWT |
| `test_register.py` | `TestRegister` | Inscription |
| `test_reset_password.py` | `TestResetPasswordEndpoints` | Réinitialisation du mot de passe |
| `test_reset_username.py` | `TestResetUsernameEndpoints` | Réinitialisation du nom d'utilisateur |
| `test_user_detail.py` | `TestUserRetrieveUser`, `TestUserUpdate`, `TestUserPatch`, `TestUserDelete` | CRUD détaillé utilisateur |
| `test_user_list.py` | `TestUserListEndpoint` | Liste des utilisateurs |
| `test_user_me.py` | `TestUserMeEndpoint`, `TestUserGetMe`, `TestUserAvatarUpdate` | Endpoint /me et avatar |

---

## Détail par fichier

### Activation de compte

**Fichier** : `test_activation.py`

```bash
python manage.py test accounts.tests.test_activation
```

Workflow d'inscription, activation de compte via uid/token, et renvoi d'email d'activation.

| Test | Description |
|------|-------------|
| `test_user_registration_and_activation` | Workflow complet : inscription → uid/token → activation |
| `test_activation_missing_uid_or_token` | Échec si uid ou token manquant |
| `test_activation_invalid_uid` | Échec avec uid invalide |
| `test_activation_invalid_token` | Échec avec token invalide |
| `test_activation_already_active_account` | Échec pour un compte déjà activé |
| `test_resend_activation_email_successful` | Renvoi d'email pour compte inactif |
| `test_resend_activation_email_missing_email` | Champ email obligatoire |
| `test_resend_activation_email_invalid_format` | Format d'email invalide |
| `test_resend_activation_unknow_email` | Email inconnu (réponse 204 pour ne pas révéler l'existence du compte) |
| `test_resend_activation_already_active_account` | Compte déjà activé (réponse 204) |

---

### Tokens JWT

**Fichier** : `test_jwt.py`

```bash
python manage.py test accounts.tests.test_jwt
```

| Test | Description |
|------|-------------|
| `test_jwt_create` | Génération de token avec identifiants valides |
| `test_jwt_create_inactive_user` | Utilisateur inactif → pas de token |
| `test_jwt_create_invalid_credentials` | Identifiants invalides → pas de token |
| `test_jwt_create_missing_fields` | Champs username/password obligatoires |
| `test_jwt_refresh` | Rafraîchissement du token |
| `test_jwt_refresh_missing_field` | Champ refresh obligatoire |
| `test_jwt_refresh_invalid_token` | Token invalide ou expiré |
| `test_jwt_verify` | Vérification de validité d'un token |
| `test_jwt_verify_invalid_token` | Token invalide → erreur |
| `test_jwt_verify_missing_field` | Champ token obligatoire |
| `test_jwt_tokens_validity` | Chaîne create → verify + refresh |

---

### Inscription

**Fichier** : `test_register.py`

```bash
python manage.py test accounts.tests.test_register
```

| Test | Description |
|------|-------------|
| `test_registration_success` | Inscription réussie avec données valides |
| `test_registration_missing_username` | Champ username obligatoire |
| `test_registration_missing_email` | Champ email obligatoire |
| `test_registration_missing_password` | Champ password obligatoire |
| `test_registration_missing_re_password` | Champ re_password obligatoire |
| `test_registration_username_invalid_characters` | Caractères non autorisés dans username |
| `test_registration_username_too_long` | Username > 150 caractères |
| `test_registration_password_similar_to_username` | Mot de passe trop proche du username |
| `test_registration_username_already_registered` | Username déjà pris |
| `test_registration_invalid_email` | Emails invalides (plusieurs formats) |
| `test_registration_email_already_registered` | Email déjà pris |
| `test_registration_passwords_do_not_match` | Mots de passe différents |
| `test_registration_password_too_short` | Mot de passe trop court |
| `test_registration_password_common` | Mots de passe trop courants |
| `test_registration_password_numeric_only` | Mot de passe uniquement numérique |

---

### Réinitialisation mot de passe

**Fichier** : `test_reset_password.py`

```bash
python manage.py test accounts.tests.test_reset_password
```

| Test | Description |
|------|-------------|
| `test_reset_password_success` | Demande de réinitialisation avec email valide |
| `test_reset_password_with_missing_email` | Champ email obligatoire |
| `test_reset_password_with_invalid_email` | Format d'email invalide |
| `test_reset_password_confirm_success` | Confirmation avec uid/token valides |
| `test_reset_password_confirm_with_missing_fields` | uid, token, new_password obligatoires |
| `test_reset_password_confirm_invalid_uid` | UID invalide |
| `test_reset_password_confirm_invalid_token` | Token invalide |
| `test_reset_password_confirm_with_expired_token` | Token expiré |
| `test_reset_password_confirm_with_weak_password` | Nouveau mot de passe trop faible |

---

### Réinitialisation nom d'utilisateur

**Fichier** : `test_reset_username.py`

```bash
python manage.py test accounts.tests.test_reset_username
```

| Test | Description |
|------|-------------|
| `test_reset_username_success` | Demande avec email valide |
| `test_reset_username_with_missing_email` | Champ email obligatoire |
| `test_reset_username_with_invalid_email` | Format d'email invalide |
| `test_reset_username_with_unknown_email` | Email inconnu (réponse 204) |
| `test_reset_username_confirm_success` | Confirmation avec uid/token/new_username valides |
| `test_reset_username_confirm_with_missing_new_username` | new_username obligatoire |
| `test_reset_username_confirm_with_missing_uid` | uid obligatoire |
| `test_reset_username_confirm_with_missing_token` | token obligatoire |
| `test_reset_username_confirm_invalid_uid` | UID invalide |
| `test_reset_username_confirm_invalid_token` | Token invalide |
| `test_reset_username_confirm_with_invalid_format_username` | Format username invalide (caractères spéciaux) |
| `test_reset_username_confirm_with_expired_token` | Token expiré |

---

### Détail, mise à jour et suppression utilisateur

**Fichier** : `test_user_detail.py`

```bash
python manage.py test accounts.tests.test_user_detail
```

#### TestUserRetrieveUser — Lecture

| Test | Description |
|------|-------------|
| `test_user_detail_success` | Accès aux détails de son propre compte |
| `test_get_user_unauthenticated` | Non authentifié → 401 |
| `test_get_user_not_found_user_id` | Utilisateur inexistant → 404 |
| `test_user_detail_own_information_as_simple_user` | Simple user accède à ses infos |
| `test_simple_user_detail_other_simple_user` | Simple user ne voit pas un autre simple user |
| `test_user_detail_as_staff_user` | Staff voit tous les utilisateurs |
| `test_user_detail_as_superuser` | Superuser voit tous les utilisateurs |

#### TestUserUpdate — PUT

| Test | Description |
|------|-------------|
| `test_put_user_update_success` | Mise à jour first_name, last_name (username non modifiable) |
| `test_put_user_update_email_switch_inactive` | Changement d'email → compte désactivé |
| `test_put_user_update_id` | ID non modifiable |
| `test_user_update_password` | Mot de passe non modifiable via PUT |
| `test_user_update_unauthenticated` | Non authentifié → 401 |
| `test_user_update_unknown_user` | Utilisateur inexistant → 404 |
| `test_user_update_as_superuser` | Superuser ne peut pas modifier un autre compte via ce endpoint |

#### TestUserPatch — PATCH

| Test | Description |
|------|-------------|
| `test_patch_user_update_success` | Mise à jour partielle |
| `test_patch_user_update_username` | Username non modifiable |
| `test_patch_user_update_password` | Mot de passe non modifiable |
| `test_patch_user_update_email` | Mise à jour email (désactive le compte) |

#### TestUserDelete — Suppression

| Test | Description |
|------|-------------|
| `test_user_delete_own_account_with_password` | Suppression avec mot de passe correct |
| `test_user_delete_unauthenticated` | Non authentifié → 401 |
| `test_user_delete_unknown_user` | Utilisateur inexistant → 404 |
| `test_user_delete_own_account_without_password` | Mot de passe obligatoire pour supprimer |
| `test_user_delete_simple_user_with_password` | Simple user ne peut pas supprimer un autre |
| `test_user_delete_other_simple_user_without_password` | Idem sans mot de passe |
| `test_staff_user_delete_simple_user_with_password` | Staff peut supprimer avec son mot de passe |
| `test_staff_user_delete_simple_user_without_password` | Staff doit fournir son mot de passe |
| `test_staff_user_delete_staff_user_with_password` | Staff peut supprimer un autre staff |
| `test_staff_user_delete_staff_user_without_password` | Mot de passe obligatoire |
| `test_superuser_delete_staff_user_with_password` | Superuser peut supprimer un staff |
| `test_superuser_delete_staff_user_without_password` | Mot de passe obligatoire |
| `test_staff_user_delete_superuser` | Staff peut supprimer un superuser |
| `test_superuser_delete_another_superuser` | Superuser peut supprimer un autre superuser |
| `test_staff_user_delete_unknown_user` | Staff → 404 pour utilisateur inconnu |
| `test_superuser_delete_unknown_user` | Superuser → 404 pour utilisateur inconnu |

---

### Liste des utilisateurs

**Fichier** : `test_user_list.py`

```bash
python manage.py test accounts.tests.test_user_list
```

| Test | Description |
|------|-------------|
| `test_simple_user_can_only_see_themselves` | Simple user ne voit que lui-même |
| `test_staff_user_can_see_all_users` | Superuser voit tous les utilisateurs |
| `test_superadmin_user_can_see_all_users` | Staff voit tous les utilisateurs |
| `test_access_user_list_unauthenticated` | Non authentifié → 401 |

---

### Endpoint /me et avatar

**Fichier** : `test_user_me.py`

```bash
python manage.py test accounts.tests.test_user_me
```

#### TestUserMeEndpoint — CRUD sur /me

| Test | Description |
|------|-------------|
| `test_get_user_me` | Récupération des infos (sans password) |
| `test_get_user_me_without_authentication` | Non authentifié → 401 |
| `test_put_user_me` | PUT complet (id/username non modifiables) |
| `test_put_user_me_unmodifiable_username` | Username non modifiable |
| `test_put_user_me_without_authentication` | Non authentifié → 401 |
| `test_put_user_me_missing_fields` | Champs obligatoires manquants |
| `test_put_user_me_invalid_email_format` | Format email invalide |
| `test_put_user_me_email_already_taken` | Email déjà pris |
| `test_patch_user_me` | PATCH partiel |
| `test_patch_user_me_without_email` | PATCH sans email (ok) |
| `test_patch_user_me_without_authentication` | Non authentifié → 401 |
| `test_patch_user_me_invalid_email_format` | Format email invalide |
| `test_patch_user_me_email_already_taken` | Email déjà pris |
| `test_delete_user_me` | Suppression du compte avec mot de passe |
| `test_delete_user_me_unauthenticated` | Non authentifié → 401 |
| `test_delete_user_me_without_password` | Mot de passe obligatoire |

#### TestUserGetMe — Rôles

| Test | Description |
|------|-------------|
| `test_user_me_as_simple_user` | Simple user accède à /me |
| `test_user_me_as_staff_user` | Staff accède à /me |
| `test_user_me_as_superuser` | Superuser accède à /me |

#### TestUserAvatarUpdate — Avatar

| Test | Description |
|------|-------------|
| `test_update_avatar_removes_old_file` | Mise à jour avatar supprime l'ancien fichier |

---

## Constantes partagées (`tests/__init__.py`)

Les messages d'erreur utilisés dans les assertions sont centralisés dans `accounts/tests/__init__.py` :

| Constante | Valeur |
|-----------|--------|
| `MANDATORY_FIELD_ERROR_MESSAGE` | 'This field is required.' |
| `INVALID_USER_ERROR_MESSAGE` | "Invalid user id or user doesn't exist." |
| `INVALID_TOKEN_ERROR_MESSAGE` | "Invalid token for given user." |
| `INVALID_EMAIL_ERROR_MESSAGE` | 'Enter a valid email address.' |
| `INVALID_USERNAME` | 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' |
| `INVALID_CREDENTIALS_ERROR_MESSAGE` | 'No active account found with the given credentials' |
| `EXPIRED_TOKEN_ERROR_MESSAGE` | 'Token is invalid or expired' |
| `USERNAME_ALREADY_TAKEN_ERROR_MESSAGE` | 'A user with that username already exists.' |
| `EMAIL_ALREADY_TAKEN_ERROR_MESSAGE` | 'user with this email already exists.' |
| `PASSWORD_TOO_SHORT_ERROR_MESSAGE` | 'This password is too short. It must contain at least 8 characters.' |
| `PASSWORD_TOO_CLOSE_USERNAME_ERROR_MESSAGE` | 'The password is too similar to the username.' |
| `TOO_COMMON_PASSWORD_ERROR_MESSAGE` | 'This password is too common.' |
| `NO_PERMISSION_ERROR_MESSAGE` | 'You do not have permission to perform this action.' |
| `AUTHENTICATION_MISSING` | "Authentication credentials were not provided." |
