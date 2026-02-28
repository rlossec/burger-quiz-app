# Wireframes — Nuggets

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [NuggetsListPage](#1-nuggetslistpage)
- [NuggetsDetailPage](#2-nuggetsdetailpage)
- [NuggetsCreatePage / NuggetsEditPage](#3-nuggetscreatepage--nuggetseditpage)
- [NuggetsForm (modale depuis BurgerQuizDetailEdit)](#4-nuggetsform-modale)
- [NuggetsQuestionInlineForm](#5-nuggetsquestioninlineform)

---

## 1 - NuggetsListPage

### Principe

Tableau des manches Nuggets : colonnes titre, original ?, nombre d'utilisation (dans un BurgerQuiz), nombre de questions. Bouton Ajouter → NuggetsCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Nuggets                              [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre questions | Actions   |
|------------------|------------|--------------|---------------|-----------|
|  Episode 123     | oui        | 2            | 6             | [👁][✏️][🗑] |
|  Culture G       | non        | 1            | 8             | [👁][✏️][🗑] |
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

```
+------------------------------------------------------------------+
|  Manche Nuggets — Culture G                                       |
+------------------------------------------------------------------+
|  Titre    : Culture G                                             |
|  Original : oui                                                   |
|                                                                   |
|  Questions (6) :                                                  |
|  ┌──────────────────────────────────────────────────────────────┐|
|  | 1. Quelle est la capitale de la France ?                     ||
|  |    A. Lyon  B. Paris ✓  C. Marseille  D. Toulouse            ||
|  ├──────────────────────────────────────────────────────────────┤|
|  | 2. Combien de continents existe-t-il ?                       ||
|  |    A. 5  B. 6  C. 7 ✓  D. 8                                   ||
|  └──────────────────────────────────────────────────────────────┘|
|  ...                                                              |
|                                                                   |
|  [Modifier]                                    [Supprimer]        |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                  | Réf.                                                    |
| ------ | ------- | ------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/nuggets/{id}/` | [api-reference](../../../backend/api-reference.md) §2.2 |

---

## 3 - NuggetsCreatePage / NuggetsEditPage

### Principe

Page dédiée pour créer/modifier une manche Nuggets. Utilise `<NuggetsForm />` avec les questions en `<NuggetsQuestionInlineForm />` par paires.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer une manche Nuggets  (ou Modifier)                          |
+------------------------------------------------------------------+
|                                                                   |
|  <NuggetsForm />                                                  |
|                                                                   |
|  Titre *   [________________________________________________]     |
|  Original  [ ] Cette manche est originale                         |
|                                                                   |
|  Questions (par paires, nombre pair requis)                       |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ Paire 1                                              [🗑]  │  |
|  │ <NuggetsQuestionInlineForm />  <NuggetsQuestionInlineForm />│  |
|  │ ┌─────────────────────────┐  ┌─────────────────────────┐  │  |
|  │ │ Q1: [________________]  │  │ Q2: [________________]  │  │  |
|  │ │ A [____] B [____]       │  │ A [____] B [____]       │  │  |
|  │ │ C [____] D [____]       │  │ C [____] D [____]       │  │  |
|  │ │ Correcte: [B ▼]         │  │ Correcte: [A ▼]         │  │  |
|  │ │ [✓ Sauvegardée]         │  │ [⏳ Non sauvée]         │  │  |
|  │ │ [Valider]               │  │ [Valider]               │  │  |
|  │ └─────────────────────────┘  └─────────────────────────┘  │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [+ Ajouter une paire de questions]                               |
|                                                                   |
|  [Annuler]                                      [Enregistrer]     |
+------------------------------------------------------------------+
```

### Appels API

| Action                                | Méthode   | Endpoint                                           | Réf.                                                    |
| ------------------------------------- | --------- | -------------------------------------------------- | ------------------------------------------------------- |
| Créer                                 | POST      | `/api/quiz/nuggets/`                               | [api-reference](../../../backend/api-reference.md) §2.2 |
| Modifier                              | PUT/PATCH | `/api/quiz/nuggets/{id}/`                          | idem                                                    |
| Questions (liste / recherche type NU) | GET       | `/api/quiz/questions/?question_type=NU&search=...` | §2.1                                                    |

---

## 4 - NuggetsForm (modale)

### Principe

Formulaire utilisé dans une modale depuis `BurgerQuizDetailEdit` pour créer ou éditer une manche Nuggets directement attachée au quiz.

### Wireframe (dans modale)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Créer une manche Nuggets                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <NuggetsForm />                                                     │
│                                                                      │
│  Titre *   [________________________________________________]        │
│  Original  [ ] Cette manche est originale                            │
│                                                                      │
│  Questions (par paires)                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ Paire 1                                              [🗑]  │     │
│  │ <NuggetsQuestionInlineForm />  <NuggetsQuestionInlineForm />│     │
│  │ [Q1: ____________]             [Q2: ____________]           │     │
│  │ [A-D + correcte]               [A-D + correcte]             │     │
│  │ [✓ Sauvegardée]                [⏳ Non sauvée]              │     │
│  │ [Valider]                      [Valider]                    │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ Paire 2                                              [🗑]  │     │
│  │ ...                                                        │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  [+ Ajouter une paire de questions]                                  │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]     │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux

```
<NuggetsModal /> (depuis BurgerQuizDetailEdit)
     │
     ▼
<NuggetsForm />
     │
     ├── Saisie titre, original
     │
     ├── Ajout de paires de questions
     │     │
     │     └── <NuggetsQuestionInlineForm /> x2
     │           ├── Saisie énoncé + 4 réponses + correcte
     │           ├── [Valider] → sauvegarde locale
     │           └── Statut affiché (✓ | ⏳ | ⚠️)
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
[[POST /api/quiz/nuggets/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { nuggets_id: newId }
     │        │
     │        ▼
     │   Fermer modale + toast "Manche créée"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs dans le formulaire
```

---

## 5 - NuggetsQuestionInlineForm

### Principe

Composant inline pour saisir une question Nuggets avec ses 4 réponses et la réponse correcte. Inclut un bouton **Valider** pour confirmer la question et un **statut de sauvegarde**.

### Props

```typescript
interface NuggetsQuestionInlineFormProps {
  question?: NuggetsQuestion; // Question existante (édition)
  index: number; // Position dans la paire
  onSave: (data: NuggetsQuestionData) => void;
  onRemove?: () => void;
}
```

### États de sauvegarde

| Statut   | Icône | Description               | Couleur |
| -------- | ----- | ------------------------- | ------- |
| `new`    | 📝    | Nouvelle question         | Gris    |
| `dirty`  | ⏳    | Non sauvegardée           | Jaune   |
| `saving` | ⏳    | Sauvegarde en cours       | Bleu    |
| `saved`  | ✓     | Sauvegardée               | Vert    |
| `error`  | ⚠️    | Erreur de validation/save | Rouge   |

### Wireframe détaillé

```
┌─────────────────────────────────────────────────────────────────┐
│  Question 1                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Énoncé *  [________________________________________________]    │
│                                                                  │
│  Réponses :                                                      │
│  A [________________________]   ○                               │
│  B [________________________]   ●  ← correcte                   │
│  C [________________________]   ○                               │
│  D [________________________]   ○                               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Statut : ✓ Sauvegardée                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Valider]                                              [🗑]     │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe compact (dans paire)

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

### Flux de validation

```
<NuggetsQuestionInlineForm />
     │
     ├── Statut initial: 📝 Nouvelle
     │
     ▼
(Saisie énoncé + réponses + correcte)
     │
     ├── Statut: ⏳ Non sauvegardée (dirty)
     │
     ▼
(Clic "Valider")
     │
     ▼
{Validation locale}
     │
     ├── ❌ Erreur
     │        │
     │        ▼
     │   Statut: ⚠️ Erreur + messages inline
     │   • "L'énoncé est requis"
     │   • "4 réponses sont requises"
     │   • "Une réponse correcte est requise"
     │
     └── ✅ Valide
              │
              ▼
         Statut: ✓ Sauvegardée (vert)
         Données stockées localement
         (envoi API au submit du formulaire parent)
```

### Validation

| Champ        | Règle                       |
| ------------ | --------------------------- |
| Énoncé       | Requis, min 10 caractères   |
| Réponses A-D | Toutes requises             |
| Correcte     | Exactement une sélectionnée |

---

## Appels API récapitulatifs

| Action                         | Méthode | Endpoint                                           | Réf. |
| ------------------------------ | ------- | -------------------------------------------------- | ---- |
| Lister manches                 | GET     | `/api/quiz/nuggets/`                               | §2.2 |
| Détail manche                  | GET     | `/api/quiz/nuggets/{id}/`                          | §2.2 |
| Créer manche                   | POST    | `/api/quiz/nuggets/`                               | §2.2 |
| Modifier manche                | PATCH   | `/api/quiz/nuggets/{id}/`                          | §2.2 |
| Supprimer manche               | DELETE  | `/api/quiz/nuggets/{id}/`                          | §2.2 |
| Rechercher questions (type NU) | GET     | `/api/quiz/questions/?question_type=NU&search=...` | §2.1 |
