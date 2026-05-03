# Wireframes — Questions

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [QuestionsListPage](#1-questionslistpage)
- [QuestionDetailPage](#2-questiondetailpage)
- [QuestionCreatePage / QuestionEditPage](#3-questioncreatepage--questioneditpage)
- [InlineQuestionForm — Pattern commun](#4-inlinequestionform--pattern-commun)

---

## 1 - QuestionsListPage

### Principe

Liste les questions avec **outil de recherche** (texte sur l'énoncé), filtres par **type** (NU, SP, ME, AD, DB) et **original** (true/false). Colonnes : texte (aperçu), type, original ?, nombre d'utilisations.

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
|  Le corbeau est...   | SP   | oui        | 1            |[👁][✏️][🗑]|
|  ...                 | ...  | ...        | ...          | ...       |
+---------------------------------------------------------------------+
|  Pagination :  < Préc  |  1  2  3  |  Suiv >                        |
+---------------------------------------------------------------------+
```

### Appels API

| Action                       | Méthode | Endpoint                                                         | Réf.                                           |
| ---------------------------- | ------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| Lister (recherche + filtres) | GET     | `/api/quiz/questions/?search=...&question_type=...&original=...` | [Lien](../../../backend/api-reference.md) §2.1 |

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

### Wireframe (type=NU)

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

### Wireframe (type=SP, ME, AD)

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

### Wireframe (type=DB)

```
+-------------------------------------------------------------------+
|  Créer une question  (ou Modifier)                                |
+-------------------------------------------------------------------+
|  Type         [ Burger de la mort (DB) ▼ ]                        |
|  Énoncé       [________________________________________________]  |
|  Original     [ ] question créée directement                      |
|  Explications [________________________________________________]  |
|  URL vidéo    [________________________________________________]  |
|  URL image    [________________________________________________]  |
|  (Pas de réponse à saisir — manche orale)                         |
|  ( Annuler )                                    ( Enregistrer )   |
+-------------------------------------------------------------------+
```

### Appels API

| Action    | Méthode   | Endpoint                    | Réf.                                                    |
| --------- | --------- | --------------------------- | ------------------------------------------------------- |
| Créer     | POST      | `/api/quiz/questions/`      | [api-reference](../../../backend/api-reference.md) §2.1 |
| Modifier  | PUT/PATCH | `/api/quiz/questions/{id}/` | idem                                                    |
| Supprimer | DELETE    | `/api/quiz/questions/{id}/` | idem                                                    |

---

## 4 - InlineQuestionForm — Pattern commun

### Principe

Les composants `InlineQuestionForm` sont utilisés **à l'intérieur** des formulaires de manches (Nuggets, Sel ou Poivre, Addition, Burger de la mort). Ils permettent de saisir des questions directement dans le contexte de la manche avec :

- Saisie des données
- Bouton **Valider** pour confirmer la question
- **Statut de sauvegarde** visible

### États de sauvegarde (commun à tous les InlineForm)

```typescript
type SaveStatus = "new" | "dirty" | "saving" | "saved" | "error";

interface QuestionInlineFormState {
  status: SaveStatus;
  isDirty: boolean;
  errors: FieldErrors;
}
```

| Statut   | Icône | Description               | Couleur | Bouton Valider |
| -------- | ----- | ------------------------- | ------- | -------------- |
| `new`    | 📝    | Nouvelle question         | Gris    | Activé         |
| `dirty`  | ⏳    | Non sauvegardée           | Jaune   | Activé         |
| `saving` | ⏳    | Sauvegarde en cours       | Bleu    | Désactivé      |
| `saved`  | ✓     | Sauvegardée               | Vert    | Activé         |
| `error`  | ⚠️    | Erreur de validation/save | Rouge   | Activé         |

### Affichage du statut

```
┌───────────────────────────────────────┐
│ Statut : [icône] [texte]              │
│          ✓       Sauvegardée          │
└───────────────────────────────────────┘
```

### Composants par type de manche

| Manche            | Composant                            | Particularités                                      |
| ----------------- | ------------------------------------ | --------------------------------------------------- |
| Nuggets           | `<NuggetsQuestionInlineForm />`      | Par paires, 4 réponses + correcte                   |
| Sel ou Poivre     | `<SaltOrPepperQuestionInlineForm />` | Réponse = dropdown des propositions                 |
| Menus             | `<MenusQuestionInlineForm />`        | Dans `MenuThemeInlineForm`, énoncé + réponse courte |
| Addition          | `<AdditionQuestionInlineForm />`     | Énoncé + réponse courte                             |
| Burger de la mort | `<DeadlyBurgerQuestionInlineForm />` | Énoncé seul (pas de réponse)                        |

> **Note Menus** : Les questions Menus sont gérées au niveau du **MenuTheme**, pas de la manche Menus directement. Le `<MenusForm />` contient 3 slots de thèmes, et c'est dans chaque `<MenuThemeInlineForm />` que l'on ajoute des `<MenusQuestionInlineForm />`.

---

### InlineQuestionForm(type=NU)

Questions Nuggets — 4 réponses + correcte, par paires.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Question 1 (NU)                                                        [🗑]  │
├───────────────────────────────────────────────────────────────────────────────┤
│  Énoncé [___________________________________________]                         │
│  A [__________] [ ]  B [__________] [X]  C [__________] [ ]  D [__________] [ ]│
│                                                                               │
│  [✓ Sauvegardée]                                               [Valider]     │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Version compacte (dans paire):**

```
┌───────────────────────────────┐  ┌───────────────────────────────┐
│ Q1: [_____________________]   │  │ Q2: [_____________________]   │
│ A [______] B [______]         │  │ A [______] B [______]         │
│ C [______] D [______]         │  │ C [______] D [______]         │
│ Correcte: [B ▼]               │  │ Correcte: [A ▼]               │
│ [✓ Sauvegardée]               │  │ [⏳ Non sauvée]               │
│ [Valider]               [🗑]  │  │ [Valider]               [🗑]  │
└───────────────────────────────┘  └───────────────────────────────┘
```

---

### InlineQuestionForm(type=SP)

Questions Sel ou Poivre — réponse = déroulant (propositions de la manche).

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Question (SP)                                                          [🗑]  │
├───────────────────────────────────────────────────────────────────────────────┤
│  Énoncé [________________________________________]  Réponse [ Noir ▼ ]        │
│                                                                               │
│  [⏳ Non sauvée]                                               [Valider]     │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

### InlineQuestionForm(type=ME, AD)

Questions Menus ou Addition — une réponse courte.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Question (ME ou AD)                                                    [🗑]  │
├───────────────────────────────────────────────────────────────────────────────┤
│  Énoncé [________________________________________]  Réponse [________________]│
│                                                                               │
│  [✓ Sauvegardée]                                               [Valider]     │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

### InlineQuestionForm(type=DB)

Questions Burger de la mort — énoncé seul (pas de réponses à saisir).

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  Question (DB)                                                          [🗑]  │
├───────────────────────────────────────────────────────────────────────────────┤
│  Énoncé [________________________________________________]                   │
│                                                                               │
│  [📝 Nouvelle]                                                 [Valider]     │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 5 - Flux de validation InlineForm

### Cycle de vie d'une question

```
[Création]
     │
     ▼
Statut: 📝 Nouvelle
     │
     ▼
(Saisie des données)
     │
     ▼
Statut: ⏳ Non sauvegardée (dirty)
     │
     ▼
(Clic "Valider")
     │
     ▼
{Validation locale}
     │
     ├── ❌ Échec validation
     │        │
     │        ▼
     │   Statut: ⚠️ Erreur
     │   Afficher messages d'erreur par champ
     │        │
     │        ▼
     │   (Correction par l'utilisateur)
     │        │
     │        ▼
     │   Statut: ⏳ Non sauvegardée (dirty)
     │   [Retour à "Clic Valider"]
     │
     └── ✅ Succès validation
              │
              ▼
         Statut: ✓ Sauvegardée
         Question stockée localement
              │
              ▼
         (Modifications ultérieures)
              │
              ▼
         Statut: ⏳ Non sauvegardée (dirty)
         [Retour à "Clic Valider"]
```

### Soumission du formulaire parent

```
[Formulaire parent (ex: NuggetsForm)]
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
{Vérification des questions}
     │
     ├── Questions avec statut ≠ "saved"
     │        │
     │        ▼
     │   Avertissement: "X questions non sauvegardées"
     │   Options:
     │     - [Valider toutes] → valide les questions dirty
     │     - [Continuer] → ignore les non-sauvées
     │     - [Annuler]
     │
     └── Toutes les questions "saved"
              │
              ▼
         Soumission API avec toutes les questions
```

---

## 6 - Validation par type de question

| Type | Champs requis                  | Validation                                       |
| ---- | ------------------------------ | ------------------------------------------------ |
| NU   | Énoncé, 4 réponses, 1 correcte | Énoncé min 10 car, toutes réponses non vides     |
| SP   | Énoncé, réponse (dropdown)     | Énoncé min 10 car, réponse dans les propositions |
| ME   | Énoncé, réponse courte         | Énoncé min 10 car, réponse non vide              |
| AD   | Énoncé, réponse courte         | Énoncé min 10 car, réponse non vide              |
| DB   | Énoncé                         | Énoncé min 10 car                                |

---

## Appels API récapitulatifs

| Action                       | Méthode | Endpoint                                                         | Réf. |
| ---------------------------- | ------- | ---------------------------------------------------------------- | ---- |
| Lister (recherche + filtres) | GET     | `/api/quiz/questions/?search=...&question_type=...&original=...` | §2.1 |
| Détail                       | GET     | `/api/quiz/questions/{id}/`                                      | §2.1 |
| Créer                        | POST    | `/api/quiz/questions/`                                           | §2.1 |
| Modifier                     | PATCH   | `/api/quiz/questions/{id}/`                                      | §2.1 |
| Supprimer                    | DELETE  | `/api/quiz/questions/{id}/`                                      | §2.1 |
