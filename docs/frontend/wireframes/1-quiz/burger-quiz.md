# Wireframes — Burger Quiz

## Burger Quiz

Pages
**BurgerQuizListPage** : Liste des Burger Quiz créés.
**BurgerQuizDetailPage** : Détail d’un quiz (titre, toss, manches liées).
**BurgerQuizCreatePage** : Création d’un quiz (titre, toss, sélection des manches : nuggets, salt_or_pepper, menus, addition, deadly_burger).
**BurgerQuizEditPage** : Édition du quiz.

### BurgerQuizListPage

On imagine une liste des burger quiz existant. On pourrait avoir une colonne indiquant son avancement (le nombre de manche fixé sur les requises : Toss, NU, ME, AD, )

### BurgerQuizListPage

Liste des sessions Burger Quiz : titre, date/création, manches incluses (aperçu). Bouton Créer. Actions : détail, édition, suppression.

### BurgerQuizDetailPage

Lecture : titre, toss, et pour chaque type de manche (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) affichage de la manche choisie (lien vers la ressource ou résumé).

### BurgerQuizCreatePage / BurgerQuizEditPage

Formulaire : titre, champ **toss** (optionnel). Champs optionnels : nuggets_id, salt_or_pepper_id, menus_id, addition_id, deadly_burger_id (listes déroulantes ou recherche vers les manches existantes). Au moins une manche recommandée.

---

## BurgerQuizListPage

```
+----------------------------------------------------------------------------+
|  Burger Quiz                                                [ + Ajouter ]  |
+----------------------------------------------------------------------------+
|  Titre              | Date création | Manches (aperçu)       | Actions     |
|---------------------|---------------|------------------------|-------------|
|  Soirée PCaT #1     | 15/02/2025    | NU, SP, ME, AD, DB    | [👁][✏️][🗑]  |
+----------------------------------------------------------------------------+
```

---

## BurgerQuizDetailPage

```
+------------------------------------------------------------------+
|  Détail Burger Quiz                                              |
+------------------------------------------------------------------+
|  Titre  Soirée PCaT #1                                           |
|  Toss   [texte du toss]                                          |
|                                                                  |
|  Manches :                                                       |
|    Nuggets         → Culture générale        [lien]              |
|    Sel ou Poivre   → Noir, Blanc ou Les deux [lien]              |
|    Menus           → Menus du jour           [lien]              |
|    Addition        → Addition rapide         [lien]              |
|    Burger de mort  → Finale                  [lien]              |
|                                                                  |
|  ( Modifier )                                   ( Supprimer )    |
+------------------------------------------------------------------+
```

---

## BurgerQuizCreatePage / BurgerQuizEditPage

```
+------------------------------------------------------------------+
|  Créer/Modifier un Burger Quiz                                   |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]       |
|  Toss   [________________________________________________]       |
|         [________________________________________________]       |
|                                                                  |
|  Manches                                                         |
|  Nuggets        [ Sélect. manche Nuggets ▼ ]       [ + Ajouter ] |
|  Sel ou Poivre  [ Sélect. manche Sel ou Poivre ▼ ] [ + Ajouter ] |
|  Menus          [ Sélect. manche Menus ▼ ]         [ + Ajouter ] |
|  Addition       [ Sélect. manche Addition ▼ ]      [ + Ajouter ] |
|  Burger de mort [ Sélect. Burger de la mort ▼ ]    [ + Ajouter ] |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )  |
+------------------------------------------------------------------+
```
