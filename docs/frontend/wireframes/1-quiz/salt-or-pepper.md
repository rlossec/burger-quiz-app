# Wireframes — Sel ou Poivre

## Sel ou Poivre

Pages :

- **SaltOrPepperListPage**
- **SaltOrPepperDetailPage**
- **SaltOrPepperCreatePage**
- **SaltOrPepperEditPage**

### SaltOrPepperListPage

Liste les manches Sel ou poivre créé, avec de même que pour les Nuggets, des colonnes original ? et e nombre d'utilisation. Enfin un bouton ajouter pour conduire vers la page d'ajout `SaltOrPepperCreatePage` et des boutons avec des icones pour aller vers SaltOrPepperDetailPage ou SaltOrPepperEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

### SaltOrPepperCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire avec le nom de la manche, trois champs par défaut les uns à côté des autres pour les propositions de réponses. On aurait un bouton pour ajouter supprimer des champs(minumum deux champs, maximum 5 champs).

Enfin une succession de champs de questions avec la réponse étant un champ déroulant avec les propositions plus haut disponibles.
On aurait aussi un case Check pour dire si c'est une question originale ou non, à la fois au niveau de la manche (et du coup si coché toutes les questions seraient cochés et pas changeable) et au niveau question.

### SaltOrPepperDetailPage

Affichage en lecture : titre, description, liste des propositions (choice_labels), liste des questions avec la réponse correcte pour chacune. Indication « original ? » (valeur dérivée à partir des questions). Boutons vers SaltOrPepperEditPage et suppression (modale).

### SaltOrPepperEditPage

Même structure que SaltOrPepperCreatePage (titre, description, 2 à 5 propositions, questions avec réponse = un des choix). Contrainte API : réponses des questions cohérentes avec les propositions. Bouton/modale pour ajouter des questions Nuggets, icônes vers détail/édition question, poubelle avec confirmation.

## SaltOrPepperListPage

Même schéma que NuggetsListPage : Titre | Original ? | Utilisations | Actions.

---

## SaltOrPepperCreatePage / SaltOrPepperEditPage

```
+----------------------------------------------------------------------+
|  Créer une manche Sel ou Poivre  (ou Modifier)                       |
+----------------------------------------------------------------------+
|  Titre       [________________________________________________]      |
|  Description [________________________________________________]      |
|  Original    [ ] oui  (si coché : toutes les questions originales)   |
|                                                                      |
|  Propositions (2 à 5)                                                |
|  [ Noir    ] [ Blanc   ] [ Les deux ]  [ + ] [ − ]                   |
|                                                                      |
|  Questions                                                           |
|  +----------------------------------------------------------------+  |
|  | Énoncé [____________________________]  Réponse [ Noir ▼ ]  [🗑] |  |
|  +----------------------------------------------------------------+  |
|  | Énoncé [__________________ _________]  Réponse [ Blanc ▼ ] [🗑] |  |
|  +----------------------------------------------------------------+  |
|  [ + Ajouter une question ]                                          |
|                                                                      |
|  ( Annuler )                                       ( Enregistrer )   |
+----------------------------------------------------------------------+
```

---

## SaltOrPepperDetailPage

```
+-------------------------------------------------------------------+
|  Détail manche Sel ou Poivre                                      |
+-------------------------------------------------------------------+
|  Titre        Noir, Blanc ou Les deux                             |
|  Description  ...                                                 |
|  Original ?   oui                                                 |
|  Propositions  Noir | Blanc | Les deux                            |
|                                                                   |
|  Questions :                                                      |
|    1. Question 1  →  Noir                                         |
|    2. Question 2  →  Blanc                                        |
|                                                                   |
|  ( Modifier )  ( Supprimer )                                      |
+-------------------------------------------------------------------+
```
