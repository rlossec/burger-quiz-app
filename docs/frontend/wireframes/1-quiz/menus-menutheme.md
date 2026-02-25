# Wireframes — Menus + MenuTheme

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [MenuThemeListPage](#1-menuthemelistpage)
- [MenuThemeDetailPage](#2-menuthemetailpage)
- [MenuThemeCreatePage / MenuThemeEditPage](#3-menuthemecreatepage--menuthemeeditpage)
- [MenuListPage](#4-menulistpage)
- [MenuDetailPage](#5-menudetailpage)
- [MenuCreatePage / MenuEditPage](#6-menucreatepage--menueditpage)

## 1 - MenuThemeListPage

### Principe

Liste des thèmes de menu (MenuTheme) : colonnes titre, type (CL/TR), original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → MenuThemeCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Thèmes de menu                                [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Type (CL/TR) | Original ? | Utilisations | Nbre Q | Actions   |
|------------------|--------------|------------|--------------|--------|-----------|
|  Gastronomie     | CL           | oui        | 1            | 3      | [👁][✏️][🗑] |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                 | Réf.                                                    |
| ------ | ------- | ------------------------ | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/menu-themes/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 2 - MenuThemeDetailPage

### Principe

Détail d’un thème : titre, type (Classique / Troll), liste ordonnée des questions. Actions : MenuThemeEditPage, suppression.

### Wireframe

_(Titre, type, liste des questions.)_

### Appels API

| Action | Méthode | Endpoint                      | Réf.                                                    |
| ------ | ------- | ----------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/menu-themes/{id}/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 3 - MenuThemeCreatePage / MenuThemeEditPage

### Principe

Pattern **InlineForm** : titre, type (CL ou TR), liste ordonnée de questions type ME. Boutons pour ajouter des questions, accéder à QuestionDetail/Edit, réordonner.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer un thème de menu  (ou Modifier)                             |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]        |
|  Type   ( ) Classique (CL)   (•) Troll (TR)                       |
|  Questions (type ME)  | # | Énoncé  | Réponse  | [👁][✏️][🗑] |   |
|  [ + Ajouter une question ]                                       |
|  ( Annuler )                                    ( Enregistrer )  |
+------------------------------------------------------------------+
```

### Appels API

| Action                    | Méthode   | Endpoint                                | Réf.                                                    |
| ------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                     | POST      | `/api/quiz/menu-themes/`                | [api-reference](../../../backend/api-reference.md) §2.4 |
| Modifier                  | PUT/PATCH | `/api/quiz/menu-themes/{id}/`           | idem                                                    |
| Questions (liste type ME) | GET       | `/api/quiz/questions/?question_type=ME` | §2.1                                                    |

---

## 4 - MenuListPage

### Principe

Liste des manches Menus : colonnes titre, original ?, nombre d’utilisation. Bouton Ajouter → MenuCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

_(Même schéma que les autres listes de manches.)_

### Appels API

| Action | Méthode | Endpoint           | Réf.                                                    |
| ------ | ------- | ------------------ | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/menus/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 5 - MenuDetailPage

### Principe

Affichage : titre, description, les 3 thèmes (menu 1, menu 2, menu troll) avec pour chacun titre et type (CL/TR), liste des questions. Actions : MenuEditPage, suppression (modale).

### Wireframe

_(Titre, description, 3 blocs thème.)_

### Appels API

| Action | Méthode | Endpoint                | Réf.                                                    |
| ------ | ------- | ----------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/menus/{id}/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 6 - MenuCreatePage / MenuEditPage

### Principe

Formulaire : titre, description optionnelle. Sélection des 3 thèmes : **menu 1** et **menu 2** (MenuTheme type CL), **menu troll** (MenuTheme type TR). Contrainte API : exactement 2 classiques + 1 troll, IDs distincts.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer une manche Menus  (ou Modifier)                            |
+------------------------------------------------------------------+
|  Titre       [________________________________________________]   |
|  Description [________________________________________________]   |
|  Menu 1 (classique)   [ Sélectionner un thème CL ▼ ]              |
|  Menu 2 (classique)   [ Sélectionner un thème CL ▼ ]              |
|  Menu troll           [ Sélectionner un thème TR  ▼ ]              |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```

### Appels API

| Action                        | Méthode   | Endpoint                 | Réf.                                                    |
| ----------------------------- | --------- | ------------------------ | ------------------------------------------------------- |
| Créer                         | POST      | `/api/quiz/menus/`       | [api-reference](../../../backend/api-reference.md) §2.4 |
| Modifier                      | PUT/PATCH | `/api/quiz/menus/{id}/`  | idem                                                    |
| Liste thèmes (pour sélection) | GET       | `/api/quiz/menu-themes/` | idem                                                    |
