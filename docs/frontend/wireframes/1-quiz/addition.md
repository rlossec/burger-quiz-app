# Wireframes — Addition

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [AdditionListPage](#1-additionlistpage)
- [AdditionDetailPage](#2-additiondetailpage)
- [AdditionCreatePage / AdditionEditPage](#3-additioncreatepage--additioneditpage)

---

## 1 - AdditionListPage

### Principe

Tableau des manches Addition avec colonnes : titre, original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → AdditionCreatePage. Icônes vers détail / édition, poubelle avec modale de confirmation.

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Addition                             [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre questions | Actions   |
|------------------|------------|--------------|---------------|-----------|
|  ...             | ...        | ...          | ...           | [👁][✏️][🗑] |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint               | Réf.                                           |
| ------ | ------- | ---------------------- | ---------------------------------------------- |
| Lister | GET     | `/api/quiz/additions/` | [lien](../../../backend/api-reference.md) §2.5 |


## 2 - AdditionDetailPage

### Principe

Affichage en lecture : titre, description, liste des questions dans l’ordre.
Actions :

- Modifier -> AdditionEditPage, suppression
- Supprimer -> modale

### Wireframe

```
+------------------------------------------------------------------+
|  Détail manche Addition                                          |
+------------------------------------------------------------------+
|  Titre       [________________________________________________]   |
|  Description [________________________________________________]   |
|  Questions :                                                      |
|    1. [________________________________________________]          |
|    2. ...                                                         |
|  ( Modifier )  ( Supprimer )                                      |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/additions/{id}/` | [lien](../../../backend/api-reference.md) §2.5 |


## 3 - AdditionCreatePage / AdditionEditPage

### Principe

Pattern **InlineForm** pour les questions ([components](../../components.md)). Formulaire : titre, description optionnelle, liste ordonnée de questions (question_ids). Questions de type AD uniquement (ex. 8 par défaut, ajout/suppression). Sélection parmi les questions existantes type AD ou création inline.

### Wireframe

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

### Appels API

| Action                           | Méthode   | Endpoint                                | Réf.                                           |
| -------------------------------- | --------- | --------------------------------------- | ---------------------------------------------- |
| Créer                            | POST      | `/api/quiz/additions/`                  | [lien](../../../backend/api-reference.md) §2.5 |
| Modifier                         | PUT/PATCH | `/api/quiz/additions/{id}/`             | idem                                           |
| Questions (liste pour sélection) | GET       | `/api/quiz/questions/?question_type=AD` | §2.1                                           |
