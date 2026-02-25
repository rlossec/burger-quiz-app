# Wireframes — Authentification

Maquettes des écrans d’authentification (Epic 1). Backend : Django REST, Djoser.

→ [../page_reference.md](../page_reference.md) · [README.md](README.md)

---

## Login

```
+------------------------------------------------------------------+
|                                                                  |
|                         Burger Quiz                              |
|                                                                  |
|              +-----------------------------------+                |
|              |  Connexion                        |                |
|              |                                   |                |
|              |  Email ou identifiant              |                |
|              |  [________________________]       |                |
|              |                                   |                |
|              |  Mot de passe                     |                |
|              |  [________________________]       |                |
|              |                                   |                |
|              |  (  Se connecter  )               |                |
|              |                                   |                |
|              |  Mot de passe oublié ? [lien]     |                |
|              |  Message erreur (si échec)        |                |
|              +-----------------------------------+                |
|                                                                  |
|              Pas de compte ? [ S'inscrire ]                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## Inscription

```
+------------------------------------------------------------------+
|                         Burger Quiz                               |
|              +-----------------------------------+                |
|              |  Créer un compte                   |                |
|              |                                   |                |
|              |  Email                            |                |
|              |  [________________________]       |                |
|              |  Identifiant (username)            |                |
|              |  [________________________]       |                |
|              |  Mot de passe                     |                |
|              |  [________________________]       |                |
|              |  Confirmer le mot de passe        |                |
|              |  [________________________]       |                |
|              |                                   |                |
|              |  (  S'inscrire  )                 |                |
|              |  Message erreur (champs invalides) |                |
|              +-----------------------------------+                |
|              Déjà un compte ? [ Se connecter ]                    |
+------------------------------------------------------------------+
```

Après succès : redirection ou message « Compte créé. Consultez votre email pour activer votre compte. »

---

## Activation du compte (lien reçu par email)

L’utilisateur clique sur le lien (uid + token). Deux cas :

**Succès**

```
+------------------------------------------------------------------+
|                         Burger Quiz                               |
|              +-----------------------------------+                |
|              |  Activation du compte              |                |
|              |                                   |                |
|              |  Votre compte est activé.         |                |
|              |  Vous pouvez vous connecter.      |                |
|              |                                   |                |
|              |  (  Se connecter  )               |                |
|              +-----------------------------------+                |
+------------------------------------------------------------------+
```

**Échec (lien invalide ou expiré)**

```
+------------------------------------------------------------------+
|              +-----------------------------------+                |
|              |  Lien invalide ou expiré          |                |
|              |  Vous pouvez demander un nouveau |                |
|              |  lien d'activation.               |                |
|              |  (  Renvoyer l'email d'activation )|                |
|              +-----------------------------------+                |
+------------------------------------------------------------------+
```

---

## Renvoi de l’email d’activation

```
+------------------------------------------------------------------+
|                         Burger Quiz                              |
|              +-----------------------------------+               |
|              |  Renvoyer l'email d'activation    |               |
|              |                                   |               |
|              |  Email du compte                  |               |
|              |  [________________________]       |               |
|              |                                   |               |
|              |  (  Envoyer  )                    |               |
|              |                                   |               |
|              |  Si un compte inactif existe,     |               |
|              |  un email a été envoyé.           |               |
|              |  (message de confirmation)        |               |
|              +-----------------------------------+               |
|              [ Retour à la connexion ]                           |
+------------------------------------------------------------------+
```

---

## Mot de passe oublié — Demande

```
+------------------------------------------------------------------+
|                         Burger Quiz                               |
|              +-----------------------------------+                |
|              |  Mot de passe oublié              |                |
|              |                                   |                |
|              |  Saisissez l'email de votre       |                |
|              |  compte :                         |                |
|              |  [________________________]       |                |
|              |                                   |                |
|              |  (  Envoyer le lien  )            |                |
|              |                                   |                |
|              |  Si un compte existe, un email    |                |
|              |  vous a été envoyé.               |                |
|              |  (message après envoi)            |                |
|              +-----------------------------------+                |
|              [ Retour à la connexion ]                            |
+-------------------------------------------------------------------+
```

---

## Mot de passe oublié — Nouveau mot de passe

Page atteinte via le lien reçu par email (uid + token dans l’URL).

```
+-------------------------------------------------------------------+
|                         Burger Quiz                               |
|              +-----------------------------------+                |
|              |  Choisir un nouveau mot de passe  |                |
|              |                                   |                |
|              |  Nouveau mot de passe             |                |
|              |  [________________________]       |                |
|              |  Confirmer le mot de passe        |                |
|              |  [________________________]       |                |
|              |                                   |                |
|              |  (  Enregistrer  )                |                |
|              |  Message erreur (lien invalide,   |                |
|              |  mots de passe différents, etc.)  |                |
|              +-----------------------------------+                |
+-------------------------------------------------------------------+
```

Après succès : message « Mot de passe modifié » + lien vers la connexion.

---

## Changer l’email (utilisateur connecté)

Page accessible depuis le profil ou les paramètres du compte.

```
+-------------------------------------------------------------------+
|  [Layout : Navbar]                                                |
|  Mon compte  >  Modifier l'email                                  |
+-------------------------------------------------------------------+
|  +-----------------------------------+                            |
|  |  Email actuel                     |                            |
|  |  user@example.com  (lecture seule)|                            |
|  |                                   |                            |
|  |  Nouvel email                    |                             |
|  |  [________________________]       |                            |
|  |                                   |                            |
|  |  (  Enregistrer  )                |                            |
|  |  Un email de confirmation sera   |                             |
|  |  envoyé au nouvel email.         |                             |
|  +-----------------------------------+                            |
+-------------------------------------------------------------------+
```

Après envoi : message « Un email de confirmation a été envoyé à [nouvel email]. Cliquez sur le lien pour valider. »

---

## Confirmation du nouvel email (lien reçu par email)

L’utilisateur clique sur le lien reçu sur le nouvel email (uid + token).

**Succès**

```
+------------------------------------------------------------------+
|              +-----------------------------------+                |
|              |  Email mis à jour                 |                |
|              |  Vous pouvez vous reconnecter     |                |
|              |  avec votre nouvel email.         |                |
|              |  (  Se connecter  )               |                |
|              +-----------------------------------+                |
+------------------------------------------------------------------+
```

**Échec** : message « Lien invalide ou expiré » + possibilité de redemander un changement d’email depuis le compte.
