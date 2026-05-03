# Wireframes — Authentification

Réf. : [page_reference](../page_reference.md) · [README](README.md). Backend : Django REST, Djoser.

## Sommaire

- [Login](#login)
- [Inscription](#inscription)
- [Activation du compte](#activation-du-compte)
- [Renvoi email d'activation](#renvoi-email-dactivation)
- [Mot de passe oublié (demande)](#mot-de-passe-oublié--demande)
- [Mot de passe oublié (nouveau)](#mot-de-passe-oublié--nouveau-mot-de-passe)
- [Changer l'email](#changer-lemail)
- [Confirmation du nouvel email](#confirmation-du-nouvel-email)

---

## Login

### Principe

Connexion par email ou identifiant + mot de passe. Lien « Mot de passe oublié », lien « S'inscrire ». Après succès : redirection vers BurgerQuizList. Message d’erreur en cas d’échec.

### Wireframe

```
+------------------------------------------------------------------+
|                         Burger Quiz                              |
|              +-----------------------------------+                |
|              |  Connexion                        |                |
|              |  Email ou identifiant  [________] |                |
|              |  Mot de passe         [________] |                |
|              |  (  Se connecter  )               |                |
|              |  Mot de passe oublié ? [lien]     |                |
|              |  Message erreur (si échec)        |                |
|              +-----------------------------------+                |
|              Pas de compte ? [ S'inscrire ]                      |
+------------------------------------------------------------------+
```

### Appels API

| Action    | Méthode | Endpoint                | Réf.                                                 |
| --------- | ------- | ----------------------- | ---------------------------------------------------- |
| Connexion | POST    | `/api/auth/jwt/create/` | [api-reference](../../backend/api-reference.md) §1.1 |

---

## Inscription

### Principe

Création de compte : email, username, mot de passe, confirmation. Compte créé mais inactif. Après succès : message « Consultez votre email pour activer votre compte ». Lien « Se connecter ».

### Wireframe

```
+------------------------------------------------------------------+
|              |  Créer un compte                   |              |
|              |  Email              [________________________]    |
|              |  Identifiant        [________________________]    |
|              |  Mot de passe      [________________________]    |
|              |  Confirmer MDP     [________________________]    |
|              |  (  S'inscrire  )   Message erreur si invalide   |
|              +-----------------------------------+              |
|              Déjà un compte ? [ Se connecter ]                    |
+------------------------------------------------------------------+
```

### Appels API

| Action      | Méthode | Endpoint           | Réf.                                                 |
| ----------- | ------- | ------------------ | ---------------------------------------------------- |
| Inscription | POST    | `/api/auth/users/` | [api-reference](../../backend/api-reference.md) §1.2 |

---

## Activation du compte

### Principe

Page atteinte via le lien reçu par email (uid + token). Succès : « Votre compte est activé », bouton Se connecter. Échec : « Lien invalide ou expiré », bouton Renvoyer l’email d’activation.

### Wireframe

Succès : message + ( Se connecter ). Échec : message + ( Renvoyer l'email d'activation ).

### Appels API

| Action            | Méthode | Endpoint                      | Réf.                                                 |
| ----------------- | ------- | ----------------------------- | ---------------------------------------------------- |
| Activer le compte | POST    | `/api/auth/users/activation/` | [api-reference](../../backend/api-reference.md) §1.3 |

---

## Renvoi email d'activation

### Principe

Champ email du compte. Bouton Envoyer. Message de confirmation neutre (« Si un compte inactif existe, un email a été envoyé »). Lien Retour à la connexion.

### Wireframe

```
+------------------------------------------------------------------+
|              |  Renvoyer l'email d'activation    |               |
|              |  Email du compte  [________]      |               |
|              |  (  Envoyer  )                    |               |
|              |  Message confirmation              |               |
|              +-----------------------------------+               |
|              [ Retour à la connexion ]                            |
+------------------------------------------------------------------+
```

### Appels API

| Action              | Méthode | Endpoint                             | Réf.                                                 |
| ------------------- | ------- | ------------------------------------ | ---------------------------------------------------- |
| Renvoyer activation | POST    | `/api/auth/users/resend_activation/` | [api-reference](../../backend/api-reference.md) §1.3 |

---

## Mot de passe oublié — Demande

### Principe

Champ email. Bouton Envoyer le lien. Message neutre après envoi. Lien Retour à la connexion.

### Wireframe

```
+------------------------------------------------------------------+
|              |  Mot de passe oublié              |               |
|              |  Email du compte [________]        |               |
|              |  (  Envoyer le lien  )            |               |
|              |  Si un compte existe, email envoyé|               |
|              +-----------------------------------+               |
|              [ Retour à la connexion ]                            |
+------------------------------------------------------------------+
```

### Appels API

| Action        | Méthode | Endpoint                          | Réf.                                                 |
| ------------- | ------- | --------------------------------- | ---------------------------------------------------- |
| Demande reset | POST    | `/api/auth/users/reset_password/` | [api-reference](../../backend/api-reference.md) §1.3 |

---

## Mot de passe oublié — Nouveau mot de passe

### Principe

Page via lien email (uid + token dans l’URL). Champs : nouveau mot de passe, confirmer. Bouton Enregistrer. Messages d’erreur (lien invalide, mots de passe différents). Après succès : message + lien vers connexion.

### Wireframe

```
+------------------------------------------------------------------+
|              |  Choisir un nouveau mot de passe  |               |
|              |  Nouveau MDP      [________]      |               |
|              |  Confirmer MDP   [________]      |               |
|              |  (  Enregistrer  )  Message erreur|               |
|              +-----------------------------------+               |
+------------------------------------------------------------------+
```

### Appels API

| Action                | Méthode | Endpoint                                  | Réf.                                                 |
| --------------------- | ------- | ----------------------------------------- | ---------------------------------------------------- |
| Confirmer nouveau MDP | POST    | `/api/auth/users/reset_password_confirm/` | [api-reference](../../backend/api-reference.md) §1.3 |

---

## Changer l'email

### Principe

Page dans l’app (utilisateur connecté). Email actuel en lecture seule, champ nouvel email. Bouton Enregistrer. Message : un email de confirmation sera envoyé au nouvel email.

### Wireframe

```
+------------------------------------------------------------------+
|  [Layout : Navbar]  Mon compte  >  Modifier l'email               |
|  Email actuel   user@example.com  (lecture seule)                |
|  Nouvel email   [________________________]                       |
|  (  Enregistrer  )  Un email de confirmation sera envoyé.       |
+------------------------------------------------------------------+
```

### Appels API

| Action         | Méthode | Endpoint                                               | Réf.                                                 |
| -------------- | ------- | ------------------------------------------------------ | ---------------------------------------------------- |
| Modifier email | PATCH   | `/api/auth/users/me/` ou `PATCH /api/auth/users/{id}/` | [api-reference](../../backend/api-reference.md) §1.2 |

---

## Confirmation du nouvel email

### Principe

Page via lien reçu sur le nouvel email (uid + token). Succès : « Email mis à jour », bouton Se connecter. Échec : « Lien invalide ou expiré ».

### Wireframe

Succès : message + ( Se connecter ). Échec : message + lien pour redemander.

### Appels API

_(Endpoint de confirmation du nouvel email — à préciser selon Djoser / custom.)_
