# Wireframes — Addition

## Addition

Pages

- **AdditionListPage**
- **AdditionCreatePage**
- **AdditionDetailPage**
- **AdditionEditPage**

### AdditionListPage

Tableau des manches Addition avec colonnes : titre, original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → AdditionCreatePage. Icônes vers détail / édition, poubelle avec modale de confirmation.

### AdditionCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, description optionnelle, liste ordonnée de questions (question_ids). Questions de type AD uniquement (ex. 8 par défaut, ajout/suppression). Sélection parmi les questions existantes type AD (ou création inline selon choix métier).

### AdditionDetailPage

Affichage : titre, description, liste des questions dans l’ordre. Valeur dérivée. Actions : AdditionEditPage, suppression (modale).

### AdditionEditPage

Même champs que AdditionCreatePage.

## Burger de la mort

- **DeadlyBurgerListPage**
- **DeadlyBurgerCreatePage**
- **DeadlyBurgerDetailPage**
- **DeadlyBurgerEditPage**

### DeadlyBurgerListPage

Tableau des manches Burger de la mort : titre, original ?, nombre d’utilisation. Bouton Ajouter → DeadlyBurgerCreatePage. Actions : détail, édition, suppression (modale).

### DeadlyBurgerCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, **10 questions** exactement (type DB). Contrainte API : 10 questions, type DB. Questions réutilisables entre manches.

### DeadlyBurgerDetailPage

Affichage : titre, liste des 10 questions dans l’ordre. Actions : DeadlyBurgerEditPage, suppression (modale).

### DeadlyBurgerEditPage

Même structure que DeadlyBurgerCreatePage (toujours 10 questions type DB).

## AdditionListPage

Colonnes : Titre | Original ? | Utilisations | Nbre questions | Actions.

## AdditionCreatePage / AdditionEditPage

```
+------------------------------------------------------------------+
|  Créer/Modifier une manche Addition                              |
+------------------------------------------------------------------+
|  Titre       [________________________________________________]  |
|  Description [________________________________________________]  |
|                                                                  |
|  Questions (type AD, 8 par défaut, ajout/suppression)            |
|  | # | Énoncé                    | Réponse courte | [🗑] |        |
|  | 1 | [______________________]  | [__________]   |     |        |
|  | 2 | [______________________]  | [__________]   |     |        |
|  ... (jusqu'à 8 ou plus)                                         |
|  [ + Ajouter une question ]                                      |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )  |
+------------------------------------------------------------------+
```
