# Wireframes — Burger Quiz

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [BurgerQuizListPage](#1-burgerquizlistpage)
- [BurgerQuizDetailPage](#2-burgerquizdetailpage)
- [BurgerQuizCreatePage / BurgerQuizEditPage](#3-burgerquizcreatepage--burgerquizeditpage)

## 1 - BurgerQuizListPage

### Principe

Liste des Burger Quiz : titre, date/création, **une colonne par manche** (Nuggets, Sel ou Poivre, Menus, Addition, Burger de la mort). Chaque manche affiche un **état** : **complet** (manche renseignée et valide), **partiel** (manche en cours ou incomplète), **absente** (aucune manche choisie). Bouton Créer. Actions : détail, édition, suppression.

### Wireframe

```
+-----------------------------------------------------------------------+
|  Burger Quiz                                           [ + Créer ]    |
+------------------------------------------------------------------ ----+
|  Titre          | Date       | NU | SP | ME | AD | BdM | Actions      |
|-----------------|------------|----|----|----|----|-----|--------------|
|  Soirée PCaT #1 | 15/02/2025 | ✅ | ✅ | ✏️| ✏️ | ✏️ | [👁][✏️][🗑]  |
|  Quiz test      | 10/02/2025 | 🚫 | 🚫 | 🚫| 🚫 | 🚫  | [👁][✏️][🗑] |
+-----------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/burger-quizzes/` | [api-reference](../../../backend/api-reference.md) §2.7 |

---

## 2 - BurgerQuizDetailPage

### Principe

Lecture : titre, toss, et pour chaque type de manche (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) affichage de la manche choisie (lien vers la ressource ou résumé).

Actions : Modifier, Supprimer.

### Wireframe

```
+------------------------------------------------------------------+
|  Détail Burger Quiz                                              |
+------------------------------------------------------------------+
|  Titre  Soirée PCaT #1                                           |
|  Toss   [texte du toss]                                          |
|  Manches :                                                       |
|    Nuggets         → Culture générale        [lien]             |
|    Sel ou Poivre   → Noir, Blanc ou Les deux [lien]              |
|    Menus           → Menus du jour           [lien]              |
|    Addition        → Addition rapide         [lien]              |
|    Burger de mort  → Finale                  [lien]              |
|  ( Modifier )                                   ( Supprimer )    |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                         | Réf.                                           |
| ------ | ------- | -------------------------------- | ---------------------------------------------- |
| Détail | GET     | `/api/quiz/burger-quizzes/{id}/` | [Lien](../../../backend/api-reference.md) §2.7 |

---

## 3 - BurgerQuizCreatePage / BurgerQuizEditPage

### Principe

Formulaire : titre, champ **toss** (optionnel). Champs optionnels : nuggets_id, salt_or_pepper_id, menus_id, addition_id, deadly_burger_id (listes déroulantes vers les manches existantes). Au moins une manche recommandée.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer/Modifier un Burger Quiz                                   |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]       |
|  Toss   [________________________________________________]       |
|  Manches                                                         |
|  Nuggets        [ Sélect. manche Nuggets ▼ ]       [ + Ajouter ] |
|  Sel ou Poivre  [ Sélect. manche Sel ou Poivre ▼ ] [ + Ajouter ] |
|  Menus          [ Sélect. manche Menus ▼ ]         [ + Ajouter ] |
|  Addition       [ Sélect. manche Addition ▼ ]      [ + Ajouter ] |
|  Burger de mort [ Sélect. Burger de la mort ▼ ]    [ + Ajouter ] |
|  ( Annuler )                                    ( Enregistrer )  |
+------------------------------------------------------------------+
```

### Appels API

| Action                          | Méthode   | Endpoint                                                                           | Réf.                                                    |
| ------------------------------- | --------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Créer                           | POST      | `/api/quiz/burger-quizzes/`                                                        | [api-reference](../../../backend/api-reference.md) §2.7 |
| Modifier                        | PUT/PATCH | `/api/quiz/burger-quizzes/{id}/`                                                   | idem                                                    |
| Listes manches (pour sélection) | GET       | `/api/quiz/nuggets/`, `salt-or-pepper/`, `menus/`, `additions/`, `deadly-burgers/` | §2.2–2.6                                                |
