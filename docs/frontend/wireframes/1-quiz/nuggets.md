# Wireframes — Nuggets

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [NuggetsListPage](#1-nuggetslistpage)
- [NuggetsDetailPage](#2-nuggetsdetailpage)
- [NuggetsCreatePage / NuggetsEditPage](#3-nuggetscreatepage--nuggetseditpage)

---

## 1 - NuggetsListPage

### Principe

Tableau des manches Nuggets : colonnes titre, original ?, nombre d’utilisation (dans un BurgerQuiz), nombre de questions. Bouton Ajouter → NuggetsCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Nuggets                              [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre questions | Actions   |
|------------------|------------|--------------|---------------|-----------|
|  Episode 123     | oui        | 2            | 6             | [👁][✏️][🗑] |
|  ...             | ...        | ...          | ...           | ...       |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint             | Réf.                                                    |
| ------ | ------- | -------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/nuggets/` | [api-reference](../../../backend/api-reference.md) §2.2 |

---

## 2 - NuggetsDetailPage

### Principe

Affichage en lecture : titre, original ?, liste des questions (énoncé + réponses, ordre). Actions : NuggetsEditPage, suppression (modale).

### Wireframe

_(Schéma identique à la liste avec zone détail : titre, questions complètes.)_

### Appels API

| Action | Méthode | Endpoint                  | Réf.                                                    |
| ------ | ------- | ------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/nuggets/{id}/` | [api-reference](../../../backend/api-reference.md) §2.2 |

---

## 3 - NuggetsCreatePage / NuggetsEditPage

### Principe

Pattern **InlineForm** ([components](../../components.md)) : questions Nuggets par **paires** (nombre pair), 2 par 2 par ligne. Chaque question : énoncé + 4 réponses (1 correcte) ou **référence à une question existante**. Contraintes : nombre pair, pas de doublon.

**Piocher dans les questions existantes** : le bouton « Ajouter une paire » ouvre une **modale** ([modale ajout question](../modals.md)) avec recherche et filtre type NU. On sélectionne une ou deux questions, on valide : les IDs sont **ajoutés à la liste** dans le formulaire ; à la **soumission** du formulaire parent, on envoie `question_ids` à l'API (une seule requête). Les questions **déjà choisies** dans la manche sont **grisées** dans la modale pour éviter les doublons.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer une manche Nuggets  (ou Modifier)                          |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]        |
|  Original  [ ] oui                                                |
|  Questions (nombre pair, 2 par 2)                                |
|  +-------------------------------+  +-------------------------------+  |
|  | Q1 [________________________] |  | Q2 [________________________] |[🗑] |
|  | 4 réponses + correcte  [👁]   |  | ou question existante [👁]   |  |
|  +-------------------------------+  +-------------------------------+  |
|  [ + Ajouter une paire ]  (ouvre modale : recherche + sélection)  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```

### Appels API

| Action                    | Méthode   | Endpoint                                | Réf.                                                    |
| ------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                     | POST      | `/api/quiz/nuggets/`                    | [api-reference](../../../backend/api-reference.md) §2.2 |
| Modifier                  | PUT/PATCH | `/api/quiz/nuggets/{id}/`               | idem                                                    |
| Questions (liste / recherche type NU) | GET | `/api/quiz/questions/?question_type=NU&search=...` | §2.1 |
