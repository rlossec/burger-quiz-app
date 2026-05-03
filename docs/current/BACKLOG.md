# Backlog

## 🍔 Vision produit

**Vision**

Permettre à un animateur de créer facilement un BurgerQuiz et d'animer des parties en direct avec ses joueurs.

**Utilisateurs**

- Animateur (Host)
- Joueurs (Players)

**Objectif MVP**

Un animateur peut :

- Créer un BurgerQuiz
- Créer les manches

## 📦 Versions

### V0.1 — Auteur (MVP)

Créer un BurgerQuiz.

- Authentification
- CRUD questions
- CRUD manches
- CRUD interludes
- CRUD BurgerQuiz

### V1.0 — Jeu

Jouer un BurgerQuiz.

- Création et gestion de Sessions
- Interface host
- Interface player

### V2.0 — Temps réel avancé

Amélioration gameplay.

- Synchronisation live
- Buzzers
- Médias

---

## État des user stories

| US            | Titre                            | Epic           | Statut |
| ------------- | -------------------------------- | -------------- | ------ |
| US-AUTH-01    | Inscription                      | 1 — Auth       | ✅     |
| US-AUTH-02    | Validation email                 | 1 — Auth       | 🚧     |
| US-AUTH-03    | Renvoi email validation          | 1 — Auth       | ✅     |
| US-AUTH-04    | Login                            | 1 — Auth       | ✅     |
| US-AUTH-05    | Mot de passe oublié              | 1 — Auth       | ✅     |
| US-AUTH-06    | Changer l’email                  | 1 — Auth       | ✅     |
| US-AUTH-07    | Changer le nom d’utilisateur     | 1 — Auth       | 🚧     |
| US-AUTH-08    | Changer le prénom                | 1 — Auth       | ✅     |
| US-AUTH-09    | Changer le nom                   | 1 — Auth       | ✅     |
| US-AUTH-10    | Changer le mot de passe          | 1 — Auth       | ✅     |
| US-BQ-01      | Liste BurgerQuiz                 | 2 — BurgerQuiz | To do  |
| US-BQ-02      | Créer BurgerQuiz                 | 2 — BurgerQuiz | To do  |
| US-BQ-03      | Modifier BurgerQuiz              | 2 — BurgerQuiz | To do  |
| US-BQ-04      | Supprimer BurgerQuiz             | 2 — BurgerQuiz | To do  |
| US-BQ-NU-01   | Ajouter une manche Nuggets       | 2 — BurgerQuiz | To do  |
| US-BQ-NU-02   | Modifier Manche Nuggets          | 2 — BurgerQuiz | To do  |
| US-BQ-SP-01   | Créer Manche Sel ou Poivre       | 2 — BurgerQuiz | To do  |
| US-BQ-SP-02   | Modifier un Manche Sel ou Poivre | 2 — BurgerQuiz | To do  |
| US-BQ-ME-01   | Créer Manche Menus               | 2 — BurgerQuiz | To do  |
| US-BQ-ME-02   | Modifier Manche Menus            | 2 — BurgerQuiz | To do  |
| US-BQ-ME-03   | Créer un MenuTheme               | 2 — BurgerQuiz | To do  |
| US-BQ-ME-04   | Modifier un MenuTheme            | 2 — BurgerQuiz | To do  |
| US-BQ-AD-01   | Créer une Manche Addition        | 2 — BurgerQuiz | To do  |
| US-BQ-AD-02   | Modifier une Manche Addition     | 2 — BurgerQuiz | To do  |
| US-BQ-DB-01   | Créer un Burger de la mort       | 2 — BurgerQuiz | To do  |
| US-GAME-01    | Créer session                    | 3 — Sessions   | To do  |
| US-GAME-02    | Rejoindre session                | 3 — Sessions   | To do  |
| US-GAME-03    | Lobby                            | 3 — Sessions   | To do  |
| US-GAME-04    | Lancer partie                    | 3 — Sessions   | To do  |
| US-HOST-01    | Voir question                    | 4 — Interface  | To do  |
| US-HOST-02    | Navigation                       | 4 — Interface  | To do  |
| US-HOST-03    | Points                           | 4 — Interface  | To do  |
| US-HOST-04    | Afficher réponse                 | 4 — Interface  | To do  |
| US-PLAYER-01  | Voir question                    | 4 — Interface  | To do  |
| US-PLAYER-02  | Voir scores                      | 4 — Interface  | To do  |
| US-PLAYER-03  | Mise à jour live                 | 4 — Interface  | To do  |
| US-UX-01      | Navigation                       | 5 — UX         | To do  |
| US-UX-02      | Messages erreurs                 | 5 — UX         | To do  |
| US-UX-03      | Loading                          | 5 — UX         | To do  |
| US-RT-01      | Synchronisation live             | 6 — Temps réel | To do  |
| US-RT-BUZZ-01 | Buzzer                           | 6 — Temps réel | To do  |
| US-RT-BUZZ-02 | Affichage buzzer                 | 6 — Temps réel | To do  |

## 1️⃣ Epics

### Epic 1 — Authentification

**Objectif** : Permettre aux utilisateurs de s'authentifier et de gérer leur compte/sécurité.

#### US-AUTH-01 Inscription

En tant qu'utilisateur

Je veux créer un compte

Afin d'utiliser l'application

Done si :

- Email obligatoire
- Username obligatoire
- Password valide
- Messages erreurs visibles
- Compte créé mais inactif

Priorité : **Must**

#### US-AUTH-02 Validation email

En tant qu'utilisateur

Je veux valider mon email

Afin d'activer mon compte

Done si :

- Email envoyé
- Lien valide
- Compte activé

**Priorité** : Must

---

#### US-AUTH-03 Renvoi email validation

Done si :

- Email renvoyé
- Message confirmation

**Priorité** : Should

#### US-AUTH-04 Login

En tant qu'utilisateur

Je veux me connecter

Afin d'accéder à mes BurgerQuiz

Done si :

- Login email ou username
- Password
- Redirection BurgerQuizList
- Message erreur

**Priorité** : Must

---

#### US-AUTH-05 Mot de passe oublié

Done si :

- Email demandé
- Email envoyé
- Reset possible

**Priorité** : Should

---

#### US-AUTH-06 Changer l’email

En tant qu’utilisateur

Je veux modifier mon adresse email

Afin de mettre à jour mon identifiant de connexion

Done si :

- Saisie du nouvel email (et confirmation si prévu)
- Compte **désactivé** jusqu’à validation du nouvel email
- **Déconnexion** immédiate après la demande de changement
- Email de validation envoyé vers la nouvelle adresse
- Messages d’erreur visibles (email déjà utilisé, format invalide, etc.)

**Priorité** : Should

---

#### US-AUTH-07 Changer le nom d’utilisateur

En tant qu’utilisateur

Je veux modifier mon nom d’utilisateur (username)

Afin d’aligner mon identifiant avec mes préférences

Done si :

- Saisie du nouveau username
- Compte **désactivé** jusqu’à revalidation du compte
- **Déconnexion** immédiate après la demande de changement
- Messages d’erreur visibles (username déjà pris, règles de format, etc.)

**Priorité** : Should

---

#### US-AUTH-08 Changer le prénom

En tant qu’utilisateur

Je veux modifier mon prénom affiché

Afin que mon profil reflète mes informations à jour

Done si :

- Champ prénom modifiable depuis le profil
- Sauvegarde persistée
- Retour utilisateur clair (succès / erreur)

**Priorité** : Could

---

#### US-AUTH-09 Changer le nom

En tant qu’utilisateur

Je veux modifier mon nom affiché

Afin que mon profil reflète mes informations à jour

Done si :

- Champ nom modifiable depuis le profil
- Sauvegarde persistée
- Retour utilisateur clair (succès / erreur)

**Priorité** : Could

---

#### US-AUTH-10 Changer le mot de passe

En tant qu’utilisateur

Je veux modifier mon mot de passe

Afin de sécuriser mon compte ou remplacer un mot de passe compromis

Done si :

- Saisie du mot de passe actuel
- Saisie du nouveau mot de passe (et confirmation)
- Règles de complexité respectées
- Ancien mot de passe incorrect rejeté avec message explicite
- Retour utilisateur clair (succès / erreur)

**Priorité** : Should

---

### Epic 2 — BurgerQuiz

**Objectif** : Créer des manches de burger quiz et des BurgerQuiz.

#### US-BQ-01 Liste BurgerQuiz

En tant qu'utilisateur

Je veux voir mes BurgerQuiz

Afin d'en sélectionner un

Done si :

- Liste affichée
- Bouton créer visible
- Liste vide gérée
- Pagination gérée

**Priorité** : Must

#### US-BQ-02 Créer BurgerQuiz

En tant qu'utilisateur

Je veux créer un BurgerQuiz

Afin de préparer un jeu

Done si :

- Champ Title
- Champ Toss
- Sauvegarde possible

**Priorité** : Must

#### US-BQ-03 Modifier BurgerQuiz

Done si :

- Modifier title
- Modifier toss

**Priorité** : Must

#### US-BQ-04 Supprimer BurgerQuiz

Done si :

- Confirmation
- Suppression OK

**Priorité** : Should

#### US-BQ-NU-01 Ajouter une manche Nuggets

En tant qu'utilisateur

Je veux ajouter une manche Nuggets

Afin de construire un BurgerQuiz

Done si :

- Choix type prérempli : Nuggets
- Des inline form ajoutable par paire avec les champs
  - intitulé
  - 4 propositions de réponses avec un checkbox correct ?

**Priorité** : Must

#### US-BQ-NU-02 Modifier Manche Nuggets

Done si :

- Choix type prérempli : Nuggets
- Des inline form ajoutable par paire avec les champs
  - intitulé
  - 4 propositions de réponses avec un checkbox correct ?

**Priorité** : Must

#### US-BQ-SP-01 Créer Manche Sel ou Poivre

En tant qu'utilisateur  
Je veux créer une manche Sel ou Poivre  
Afin de proposer des questions à choix restreints

Done si :

- Titre
- 2 à 5 propositions (ajout/suppression possible)
- Questions avec réponse = une des propositions (inline)
- Ajouter / supprimer des questions inline

**Priorité** : Must

#### US-BQ-SP-02 Modifier un Manche Sel ou Poivre

En tant qu'utilisateur  
Je veux modifier une manche Sel ou Poivre  
Afin de proposer des questions à choix restreints

Done si :

- Titre
- 2 à 5 propositions (ajout/suppression possible)
- Questions avec réponse = une des propositions (inline)
- Ajouter / supprimer des questions inline

**Priorité** : Must

#### US-BQ-ME-01 Créer Manche Menus

En tant qu'utilisateur  
Je veux créer une manche Menus  
Afin d'associer deux menus classiques et un menu troll

Done si :

- Titre, description optionnelle
- Sélection de 2 thèmes classiques (CL) et 1 thème troll (TR)
- Les thèmes existent ou sont créés via MenuTheme

#### US-BQ-ME-02 Modifier Manche Menus

En tant qu'utilisateur

Je veux modifier une manche Menus

Afin d'associer deux menus classiques et un menu troll

Done si :

- Titre, description optionnelle
- Sélection de 2 thèmes classiques (CL) et 1 thème troll (TR)
- Les thèmes existent ou sont créés via MenuTheme

#### US-BQ-ME-03 Créer un MenuTheme

En tant qu'utilisateur  
Je veux créer un thème de menu (MenuTheme)  
Afin de l'utiliser dans une manche Menus

Done si :

- Titre, type (CL ou TR)
- Questions type ME (inline, ajouter/supprimer)

#### US-BQ-ME-04 Modifier un MenuTheme

En tant qu'utilisateur  
Je veux modifier un thème de menu (MenuTheme)  
Afin de l'utiliser dans une manche Menus

Done si :

- Titre, type (CL ou TR)
- Questions type ME (inline, ajouter/supprimer)

#### US-BQ-AD-01 Créer une Manche Addition

En tant qu'utilisateur  
Je veux créer une manche Addition  
Afin d'ajouter des questions à réponse courte

Done si :

- Titre, description optionnelle
- Questions type AD (ex. 8 inline par défaut, ajouter/supprimer)

#### US-BQ-AD-02 Modifier une Manche Addition

En tant qu'utilisateur  
Je veux Modifier une manche Addition  
Afin d'ajouter des questions à réponse courte

Done si :

- Titre, description optionnelle
- Questions type AD (ex. 8 inline par défaut, ajouter/supprimer)

**Priorité** : Must

#### US-BQ-DB-01 Créer un Burger de la mort

En tant qu'utilisateur  
Je veux créer une manche Burger de la mort  
Afin de constituer la finale

Done si :

- Titre
- Exactement 10 questions type DB (inline)

**Priorité** : Must

### Epic 3 — Sessions de jeu

**Objectif** : Jouer un BurgerQuiz.

#### US-GAME-01 Créer session

En tant qu'hôte

Je veux créer une session

Afin de jouer

Done si :

- Choix BurgerQuiz
- Session créée
- Hôte défini

**Priorité** : Must (V0.2)

#### US-GAME-02 Rejoindre session

En tant que joueur

Je veux rejoindre une session

Done si :

- Code session
- Nom joueur

**Priorité** : Must

#### US-GAME-03 Lobby

Done si :

- Liste joueurs
- Host visible

**Priorité** : Must

#### US-GAME-04 Lancer partie

Done si :

- Partie démarre

**Priorité** : Must

### Epic 4 — Interface

**Objectif** : Animer la partie.

#### US-HOST-01 Voir question

Done si :

- Question visible
- Réponse cachée

**Priorité** : Must

#### US-HOST-02 Navigation

Done si :

- Question suivante
- Question précédente

**Priorité** : Must

#### US-HOST-03 Points

Done si :

- Ajouter points
- Retirer points

**Priorité** : Must

#### US-HOST-04 Afficher réponse

Done si :

- Réponse visible

**Priorité** : Must

#### US-PLAYER-01 Voir question

Done si :

- Question visible

**Priorité** : Must

#### US-PLAYER-02 Voir scores

Done si :

- Scores visibles

**Priorité** : Must

#### US-PLAYER-03 Mise à jour live

Done si :

- Mise à jour automatique

**Priorité** : Should

### Epic 5 — UX

Souvent oublié.

#### US-UX-01 Navigation

Done si :

- Navbar
- Logout
- BurgerQuiz accessible

Priorité :

Must

#### US-UX-02 Messages erreurs

Done si :

- Erreurs lisibles

Priorité :

Must

#### US-UX-03 Loading

Done si :

- Loader visible

Priorité :

Should

### Epic 6 — Temps réel (V2.0)

**Objectif** : Améliorer le gameplay.

#### US-RT-01 Synchronisation live

Done si :

- Host synchronise players

**Priorité** : Should

#### US-RT-BUZZ-01 Buzzer

Done si :

- Bouton buzzer
- Premier enregistré

**Priorité** : Could

#### US-RT-BUZZ-02 Affichage buzzer

Done si :

- Nom affiché

**Priorité** : Could

### Parcours utilisateur (résumé)

| Étape | Description                                                                    | Page / flux                |
| ----- | ------------------------------------------------------------------------------ | -------------------------- |
| 1     | S'authentifier                                                                 | Login → BurgerQuizList     |
| 2     | Consulter les Burger Quiz                                                      | BurgerQuizList             |
| 3     | Créer un Burger Quiz (titre, toss, manches)                                    | BurgerQuizCreate           |
| 4     | Créer des manches (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) | Pages de création par type |

Détail des pages et du flux (inline forms, structure) : [../frontend/page_reference.md](../frontend/page_reference.md) et [../frontend/components.md](../frontend/components.md).
