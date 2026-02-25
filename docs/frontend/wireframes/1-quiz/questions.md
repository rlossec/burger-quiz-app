# Wireframes — Questions

## Question

Pages :

- **QuestionsListPage** : Liste les questions avec des filtres de type, original.
- **QuestionDetailPage** : Détail d’une question (énoncé, réponses, type, original, médias).
- **QuestionCreatePage** : Création d’une question (type, énoncé, réponses, original, video_url, image_url).
- **QuestionEditPage** : Édition de la question sélectionnée.

### QuestionsListPage

Liste les questions avec des filtres par **type** (NU, SP, ME, AD, DB), **original** (true/false). Colonnes possibles : texte (aperçu), type, original ?, nombre d'utilisations, nombre d’utilisations. Actions : accès au détail, édition, suppression (avec modale de confirmation). Bouton « Ajouter » pour aller vers QuestionCreatePage.

### QuestionDetailPage

Affichage en lecture seule : texte de la question, type, original ?, explications, liens vidéo/image, liste des réponses avec indication de la bonne réponse. Liens ou boutons vers QuestionEditPage et retour à la liste.

### QuestionCreatePage / QuestionEditPage

Formulaire : type de question (sélection), énoncé, original (case à cocher), explications optionnelles, video_url et image_url optionnels. Bloc réponses selon le type (ex. 4 réponses pour NU, 2 pour SP, etc.) avec indication de la réponse correcte.

Voir [../page_reference.md#question](../page_reference.md) et [../components.md](../components.md).

---

## QuestionsListPage

```
+------------------------------------------------------------------+
|  Navbar                                                          |
+------------------------------------------------------------------+
|  Questions                                    [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Filtres :  Type [ NU ▼ ]  Original [ Tous ▼ ]  [ Appliquer ]    |
+------------------------------------------------------------------+
|  Texte (aperçu)      | Type | Original ? | Utilisations | Actions |
|----------------------|------|------------|--------------|--------|
|  Quelle est la...    | NU   | oui        | 2            | [👁][✏️][🗑] |
|  Noir ou Blanc ?     | SP   | non        | 1            | [👁][✏️][🗑] |
|  ...                 | ...  | ...        | ...          | ...    |
+------------------------------------------------------------------+
|  Pagination :  < Préc  |  1  2  3  |  Suiv >                      |
+------------------------------------------------------------------+
```

---

## QuestionDetailPage

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
|                                                                  |
|  Réponses :                                                      |
|    • Paris     [correcte]                                         |
|    • Lyon                                                         |
|    • Marseille                                                    |
|    • Toulouse                                                     |
|                                                                  |
|  ( Retour liste )    ( Modifier )                                 |
+------------------------------------------------------------------+
```

---

## QuestionCreatePage / QuestionEditPage

```
+------------------------------------------------------------------+
|  Créer une question  (ou Modifier)                                |
+------------------------------------------------------------------+
|  Type         [ Nuggets (NU) ▼ ]                                  |
|  Énoncé       [________________________________________________]  |
|  Original     [ ] question créée directement                      |
|  Explications [________________________________________________]  |
|  URL vidéo    [________________________________________________]  |
|  URL image    [________________________________________________]  |
|                                                                  |
|  Réponses (4 pour NU) :         Correcte ?                       |
|    [________________________]   ( ) A  (•) B  ( ) C  ( ) D       |
|    [________________________]   ou checkbox par ligne            |
|    [________________________]                                    |
|    [________________________]                                    |
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```
