# Wireframes — Modales

Réf. : [components](../components.md) · [README](README.md)

## Sommaire

- [Modale de confirmation (suppression)](#modale-de-confirmation-suppression)
- [Modale ajout question](#modale-ajout-question)

---

## Modale de confirmation (suppression)

### Principe

Demande de confirmation avant suppression d'une ressource (manche, question, Burger Quiz, etc.). Affiche le nom de la ressource et son type. Boutons Annuler et Supprimer.

### Wireframe

```
+------------------------------------------+
|  Confirmer la suppression                |
+------------------------------------------+
|  Êtes-vous sûr de vouloir supprimer      |
|  « Culture générale » ?                  |
|  (Manche Nuggets)                        |
|  ( Annuler )            ( Supprimer )    |
+------------------------------------------+
```

### Appels API

Selon la ressource : `DELETE /api/quiz/{resource}/{id}/` (questions, nuggets, salt-or-pepper, menus, menu-themes, additions, deadly-burgers, burger-quizzes). Voir [api-reference](../../backend/api-reference.md).

---

## Modale ajout question

### Principe

Permet d'ajouter des questions à une manche (Nuggets, Deadly Burger, etc.) : **sélectionner des questions existantes** via un **outil de recherche**, ou créer une nouvelle question (inline / nouvelle page selon choix). Les questions sélectionnées sont **ajoutées à la liste** du formulaire parent ; les IDs sont envoyés **lors de la soumission** du formulaire (pas de sauvegarde dans cette modale).

**Outil de recherche** : champ de recherche (texte sur l'énoncé), filtre par type (prérempli selon la manche : NU, DB, etc.), résultats paginés avec case à cocher. Les questions déjà présentes dans la manche peuvent être grisées / non sélectionnables pour éviter les doublons.

### Wireframe

```
+-----------------------------------------------------------------------------+
|  Ajouter des questions (Nuggets / Burger de la mort / …)                    |
+-----------------------------------------------------------------------------+
|  Recherche    [_________________________________________]  [ 🔍 ]           |
|  Type         [ Nuggets (NU) ▼ ]  (prérempli selon la manche)               |
|  +-----------------------------------------------------------------------+  |
|  | Résultats (questions existantes)                                      |  |
|  | [ ] Quelle est la capitale…        NU   (déjà dans la manche → grisé) |  |
|  | [X] Paris est la capitale de…      NU                                  |  |
|  | [ ] La France a pour chef d'État…  NU                                  |  |
|  |  < Préc  |  1  2  3  |  Suiv >                                          |  |
|  +-----------------------------------------------------------------------+  |
|  ( ) Créer une nouvelle question  (optionnel, selon flux)                 |
|  ( Annuler )                                    ( Valider )                |
+-----------------------------------------------------------------------------+
```

### Appels API

| Action                      | Méthode | Endpoint                                            | Réf.                                                 |
| --------------------------- | ------- | --------------------------------------------------- | ---------------------------------------------------- |
| Recherche / liste questions | GET     | `/api/quiz/questions/?question_type=...&search=...` | [api-reference](../../backend/api-reference.md) §2.1 |

À la validation : la modale retourne les IDs sélectionnés au formulaire parent ; aucun appel API dans la modale. La soumission du formulaire parent envoie `question_ids` (POST/PUT manche).
