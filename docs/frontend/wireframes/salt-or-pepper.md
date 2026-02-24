# Wireframes — Sel ou Poivre

Voir [../page_reference.md#sel-ou-poivre](../page_reference.md) et [../components.md](../components.md).

---

## SaltOrPepperListPage

Même schéma que NuggetsListPage : Titre | Original ? | Utilisations | Actions.

---

## SaltOrPepperCreatePage / SaltOrPepperEditPage

```
+------------------------------------------------------------------+
|  Créer une manche Sel ou Poivre  (ou Modifier)                    |
+------------------------------------------------------------------+
|  Titre       [________________________________________________]   |
|  Description [________________________________________________]   |
|  Original    [ ] oui  (si coché : toutes les questions originales) |
|                                                                  |
|  Propositions (2 à 5)                                             |
|  [ Noir    ] [ Blanc   ] [ Les deux ]  [ + ] [ − ]                |
|                                                                  |
|  Questions                                                        |
|  +----------------------------------------------------------------+  |
|  | Énoncé [________________________________________]  Réponse [ Noir ▼ ]  [🗑] |  |
|  +----------------------------------------------------------------+  |
|  | Énoncé [________________________________________]  Réponse [ Blanc ▼ ]  [🗑] |  |
|  +----------------------------------------------------------------+  |
|  [ + Ajouter une question ]                                       |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```

---

## SaltOrPepperDetailPage

```
+------------------------------------------------------------------+
|  Détail manche Sel ou Poivre                                      |
+------------------------------------------------------------------+
|  Titre        Noir, Blanc ou Les deux                             |
|  Description  ...                                                 |
|  Original ?   oui                                                 |
|  Propositions  Noir | Blanc | Les deux                            |
|                                                                  |
|  Questions :                                                      |
|    1. Question 1  →  Noir                                          |
|    2. Question 2  →  Blanc                                         |
|                                                                  |
|  ( Modifier )  ( Supprimer )                                      |
+------------------------------------------------------------------+
```
