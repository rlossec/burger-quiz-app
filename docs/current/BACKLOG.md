# Backlog

Backlog orienté utilisateur.

Objectif :
Transformer les parcours utilisateur en travail finissable.

---

## Epics

| Epic | Description | Version |
|------|-------------|---------|
| BurgerQuiz CRUD | Créer et gérer des Burger Quiz | V0.1 |
| Rounds CRUD | Créer les manches | V0.1 |
| Questions CRUD | Créer les questions | V0.1 |
| Game Sessions | Jouer un BurgerQuiz | V0.2 |

---

## User Stories

### Auth

#### US-01 Login

En tant qu'utilisateur  
Je veux me connecter  
Afin d'accéder à mes BurgerQuiz

Done si :

- Login fonctionne
- Redirection vers BurgerQuizList
- Message erreur si mauvais password

---

### BurgerQuiz

#### US-02 Liste BurgerQuiz

En tant qu'utilisateur  
Je veux voir mes BurgerQuiz  
Afin d'en sélectionner un

Done si :

- Liste affichée
- Bouton créer visible

---

#### US-03 Créer BurgerQuiz

En tant qu'utilisateur  
Je veux créer un BurgerQuiz  
Afin de préparer un jeu

Done si :

- Champ title
- Champ toss
- Sauvegarde possible

---

### Rounds

#### US-04 Créer Manche Nuggets

En tant qu'utilisateur  
Je veux créer une manche Nuggets  
Afin d'ajouter des questions

Done si :

- Titre
- Nombre pair de questions (ex. 6 possibles)
- Ajouter / supprimer des questions inline

→ Détail des composants (InlineForm) : [../frontend/components.md](../frontend/components.md). Structure des pages : [../frontend/page_reference.md](../frontend/page_reference.md).

---

#### US-05 Créer Manche Sel ou Poivre

En tant qu'utilisateur  
Je veux créer une manche Sel ou Poivre  
Afin de proposer des questions à choix restreints

Done si :

- Titre
- 2 à 5 propositions (ajout/suppression possible)
- Questions avec réponse = une des propositions (inline)
- Ajouter / supprimer des questions inline

---

#### US-06 Créer Manche Menus

En tant qu'utilisateur  
Je veux créer une manche Menus  
Afin d'associer deux menus classiques et un menu troll

Done si :

- Titre, description optionnelle
- Sélection de 2 thèmes classiques (CL) et 1 thème troll (TR)
- Les thèmes existent ou sont créés via MenuTheme

---

#### US-07 Créer MenuTheme

En tant qu'utilisateur  
Je veux créer un thème de menu (MenuTheme)  
Afin de l'utiliser dans une manche Menus

Done si :

- Titre, type (CL ou TR)
- Questions type ME (inline, ajouter/supprimer)

---

#### US-08 Créer Manche Addition

En tant qu'utilisateur  
Je veux créer une manche Addition  
Afin d'ajouter des questions à réponse courte

Done si :

- Titre, description optionnelle
- Questions type AD (ex. 8 inline par défaut, ajouter/supprimer)

---

#### US-09 Créer Manche Burger de la mort

En tant qu'utilisateur  
Je veux créer une manche Burger de la mort  
Afin de constituer la finale

Done si :

- Titre
- Exactement 10 questions type DB (inline)

---

### Parcours utilisateur (résumé)

| Étape | Description | Page / flux |
|-------|-------------|-------------|
| 1 | S'authentifier | Login → BurgerQuizList |
| 2 | Consulter les Burger Quiz | BurgerQuizList |
| 3 | Créer un Burger Quiz (titre, toss, manches) | BurgerQuizCreate |
| 4 | Créer des manches (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) | Pages de création par type |

Détail des pages et du flux (inline forms, structure) : [../frontend/page_reference.md](../frontend/page_reference.md) et [../frontend/components.md](../frontend/components.md).

---

### Références techniques

- **Ordre des appels API** et contraintes : [../backend/api-reference.md](../backend/api-reference.md) §2 (Quiz).
- **Contraintes métier** : SP, ME, AD = une question une manche ; NU, DB = questions réutilisables. Détail dans api-reference.
