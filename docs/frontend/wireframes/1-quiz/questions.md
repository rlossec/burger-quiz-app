# Wireframes — Questions

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [QuestionsListPage](#1-questionslistpage)
- [QuestionDetailPage](#2-questiondetailpage)
- [QuestionCreatePage / QuestionEditPage](#3-questioncreatepage--questioneditpage)

---

## 1 - QuestionsListPage

### Principe

Liste les questions avec **outil de recherche** (texte sur l’énoncé), filtres par **type** (NU, SP, ME, AD, DB) et **original** (true/false). Colonnes : texte (aperçu), type, original ?, nombre d’utilisations.

Actions : accès au détail, édition, suppression (modale). Bouton « Ajouter » → QuestionCreatePage.

### Wireframe

```
+---------------------------------------------------------------------+
|  Questions                                    [ + Ajouter ]         |
+---------------------------------------------------------------------+
|  Recherche  [________________________________________]  [ 🔍 ]      |
|  Filtres :  Type [ NU ▼ ]  Original [ Tous ▼ ]  [ Appliquer ]       |
+---------------------------------------------------------------------+
|  Texte (aperçu)      | Type | Original ? | Utilisations |  Actions  |
|----------------------|------|------------|--------------|-----------|
|  Quelle est la...    | NU   | oui        | 2            |[👁][✏️][🗑]|
|  ...                 | ...  | ...        | ...          | ...       |
+---------------------------------------------------------------------+
|  Pagination :  < Préc  |  1  2  3  |  Suiv >                        |
+---------------------------------------------------------------------+
```

### Appels API

| Action                | Méthode | Endpoint                                                              | Réf.                                           |
| --------------------- | ------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| Lister (recherche + filtres) | GET | `/api/quiz/questions/?search=...&question_type=...&original=...` | [Lien](../../../backend/api-reference.md) §2.1 |

---

## 2 - QuestionDetailPage

### Principe

Affichage en lecture seule : texte de la question, type, original ?, explications, liens vidéo/image, liste des réponses avec indication de la bonne réponse. Liens vers QuestionEditPage et retour à la liste.

### Wireframe

```
+------------------------------------------------------------------+
|  Questions  >  Détail                                             |
+------------------------------------------------------------------+
|  Texte        [________________________________________________]  |
|  Type         NU (Nuggets)                                        |
|  Original ?   [x] oui                                             |
|  Explications [________________________________________________]  |
|  Vidéo        https://...                                         |
|  Image        https://...                                         |
|  Réponses :   • Paris [correcte]  • Lyon  • Marseille  • Toulouse |
|  ( Retour liste )    ( Modifier )                                 |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/questions/{id}/` | [api-reference](../../../backend/api-reference.md) §2.1 |

---

## 3 - QuestionCreatePage / QuestionEditPage

### Principe

Formulaire : type de question (sélection), énoncé, original (case à cocher), explications optionnelles, video_url et image_url optionnels. Bloc réponses selon le type (ex. 4 réponses pour NU) avec indication de la réponse correcte.

### Wireframe

version : QuestionForm(type=NU)

```
+-------------------------------------------------------------------+
|  Créer une question  (ou Modifier)                                |
+-------------------------------------------------------------------+
|  Type         [ Nuggets (NU) ▼ ]                                  |
|  Énoncé       [________________________________________________]  |
|  Original     [ ] question créée directement                      |
|  Explications [________________________________________________]  |
|  URL vidéo    [________________________________________________]  |
|  URL image    [________________________________________________]  |
|  Réponses (4 pour NU) :         Correcte ?                        |
|  A [________________________]   [ ]                               |
|  B [________________________]   [X]                               |
|  C [________________________]   [ ]                               |
|  D [________________________]   [ ]                               |
|  ( Annuler )                                    ( Enregistrer )   |
+-------------------------------------------------------------------+
```

QuestionForm(type=SP,ME,AD,DB)

```
+-------------------------------------------------------------------+
|  Créer une question  (ou Modifier)                                |
+-------------------------------------------------------------------+
|  Type         [ Sel ou Poivre (SP) ▼ ]                            |
|  Énoncé       [________________________________________________]  |
|  Original     [ ] question créée directement                      |
|  Explications [________________________________________________]  |
|  URL vidéo    [________________________________________________]  |
|  URL image    [________________________________________________]  |
|  Réponse      [________________________________________________]  |
|  ( Annuler )                                    ( Enregistrer )   |
+-------------------------------------------------------------------+
```

#### Équivalents InlineQuestionForm

Utilisés **à l’intérieur** d’un formulaire de manche (Nuggets, Sel ou Poivre, MenuTheme, Addition, Burger de la mort). Le type est **prérempli** selon la page, non modifiable. Une ligne (ou un bloc) par question, avec [🗑] pour supprimer. Voir [components.md](../../components.md) (QuestionsInlineForm).

**InlineQuestionForm(type=NU)** — une ligne par question, 4 réponses + correcte (ex. Nuggets, 2 par 2) :

```
+--------------------------------------------------------------------------------------------------------+
|  Question 1(NU)                                                                                  [🗑]   |
|  Énoncé [___________]  A [__________] [ ]  B [__________] [X]  C [__________] [ ]  D [__________] [ ]  |
+--------------------------------------------------------------------------------------------------------+
```

**InlineQuestionForm(type=SP)** — réponse = déroulant (propositions de la manche) :

```
+--------------------------------------------------------------------------------------------------+
|  Question (SP)                                                                             [🗑]   |
|  Énoncé [________________________________________]  Réponse [ Noir ▼ ]                           |
+--------------------------------------------------------------------------------------------------+
```

**InlineQuestionForm(type=ME, AD)** — une réponse courte :

```
+--------------------------------------------------------------------------------------------------+
|  Question (ME ou AD)                                                                       [🗑]   |
|  Énoncé [________________________________________]  Réponse [________________]                   |
+--------------------------------------------------------------------------------------------------+
```

**InlineQuestionForm(type=DB)** — énoncé seul (pas de réponses à saisir) :

```
+--------------------------------------------------------------------------------------------------+
|  Question (DB)                                                                             [🗑]   |
|  Énoncé [________________________________________________]                                      |
+--------------------------------------------------------------------------------------------------+
```

### Appels API

| Action    | Méthode   | Endpoint                    | Réf.                                                    |
| --------- | --------- | --------------------------- | ------------------------------------------------------- |
| Créer     | POST      | `/api/quiz/questions/`      | [api-reference](../../../backend/api-reference.md) §2.1 |
| Modifier  | PUT/PATCH | `/api/quiz/questions/{id}/` | idem                                                    |
| Supprimer | DELETE    | `/api/quiz/questions/{id}/` | idem                                                    |
