# Wireframes — Menus + MenuTheme

## Menus

Pages :

- **MenuListPage**
- **MenuCreatePage**
- **MenuDetailPage**
- **MenuEditPage**
- **MenuThemeListPage**
- **MenuThemeDetailPage**
- **MenuThemeCreatePage**
- **MenuThemeEditPage**

### MenuListPage

Dans la même configuration que pour les autres pages on aurait un listing des manche Menu avec la colonne "original ?" et "nombre d'utilisation".
On aurait ensuite un bouton Ajouter pour aller vers la page MenuCreatePage au dessus du listing, et des boutons avec des icones pour aller vers MenuDetailPage ou MenuEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

### MenuDetailPage

Affichage : titre, description, et les 3 thèmes (menu 1, menu 2, menu troll) avec pour chacun titre et type (CL/TR), liste des questions. Valeur dérivée « original ? ». Actions : MenuEditPage, suppression (modale).

### MenuCreatePage

Formulaire : titre, description optionnelle. Sélection des 3 thèmes : **menu 1** et **menu 2** (MenuTheme avec type CL), **menu troll** (MenuTheme avec type TR). Les thèmes doivent être créés au préalable (MenuThemeCreatePage) ou sélectionnés parmi la liste. Contrainte API : exactement 2 classiques + 1 troll, IDs distincts.

### MenuEditPage

Même champs que MenuCreatePage (titre, description, menu_1_id, menu_2_id, menu_troll_id). Réutilisation des mêmes contraintes.

### MenuThemeListPage

Liste des thèmes de menu (MenuTheme) avec colonnes : titre, type (CL / TR), original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → MenuThemeCreatePage. Actions : détail, édition, suppression (modale).

### MenuThemeDetailPage

Détail d’un thème : titre, type (Classique / Troll), liste ordonnée des questions. Actions : MenuThemeEditPage, suppression.

### MenuThemeCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, type (CL ou TR), liste ordonnée de questions (question_ids). Questions de type ME uniquement. Boutons/liens pour ajouter des questions, accéder à QuestionDetail/Edit, réordonner.

### MenuThemeEditPage

Même structure que MenuThemeCreatePage.

---

## MenuThemeListPage

```
+------------------------------------------------------------------+
|  Thèmes de menu                                [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Type (CL/TR) | Original ? | Utilisations | Nbre Q | Actions   |
|------------------|--------------|------------|--------------|--------|-----------|
|  Gastronomie     | CL           | oui        | 1            | 3      | [👁][✏️][🗑] |
+------------------------------------------------------------------+
```

---

## MenuThemeCreatePage / MenuThemeEditPage (InlineForm ME)

```
+------------------------------------------------------------------+
|  Créer un thème de menu  (ou Modifier)                             |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]        |
|  Type   ( ) Classique (CL)   (•) Troll (TR)                        |
|                                                                  |
|  Questions (type ME)                                              |
|  | # | Énoncé                    | Réponse      | [👁][✏️][🗑] |  |
|  | 1 | [______________________]  | [__________] |             |  |
|  | 2 | [______________________]  | [__________] |             |  |
|  [ + Ajouter une question ]                                       |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```

---

## MenuCreatePage / MenuEditPage

```
+------------------------------------------------------------------+
|  Créer une manche Menus  (ou Modifier)                             |
+------------------------------------------------------------------+
|  Titre       [________________________________________________]   |
|  Description [________________________________________________]   |
|                                                                  |
|  Menu 1 (classique)   [ Sélectionner un thème CL ▼ ]              |
|  Menu 2 (classique)   [ Sélectionner un thème CL ▼ ]              |
|  Menu troll           [ Sélectionner un thème TR  ▼ ]              |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```
