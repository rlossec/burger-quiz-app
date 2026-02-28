# Wireframes — Addition

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [AdditionListPage](#1-additionlistpage)
- [AdditionDetailPage](#2-additiondetailpage)
- [AdditionCreatePage / AdditionEditPage](#3-additioncreatepage--additioneditpage)
- [AdditionForm (modale depuis BurgerQuizDetailEdit)](#4-additionform-modale)
- [AdditionQuestionInlineForm](#5-additionquestioninlineform)

---

## 1 - AdditionListPage

### Principe

Tableau des manches Addition avec colonnes : titre, original ?, nombre d'utilisation, nombre de questions. Bouton Ajouter → AdditionCreatePage. Icônes vers détail / édition, poubelle avec modale de confirmation.

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Addition                             [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre questions | Actions   |
|------------------|------------|--------------|---------------|-----------|
|  Addition rapide | oui        | 2            | 8             | [👁][✏️][🗑] |
|  Calcul mental   | non        | 1            | 10            | [👁][✏️][🗑] |
|  ...             | ...        | ...          | ...           | ...       |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint               | Réf.                                                    |
| ------ | ------- | ---------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/additions/` | [api-reference](../../../backend/api-reference.md) §2.5 |

---

## 2 - AdditionDetailPage

### Principe

Affichage en lecture : titre, description, liste des questions dans l'ordre (énoncé + réponse courte).
Actions : Modifier → AdditionEditPage, Supprimer → modale.

### Wireframe

```
+------------------------------------------------------------------+
|  Manche Addition — Addition rapide                                |
+------------------------------------------------------------------+
|  Titre       : Addition rapide                                    |
|  Description : Questions de calcul mental                         |
|  Original    : oui                                                |
|                                                                   |
|  Questions (8) :                                                  |
|  ┌────────────────────────────────────────────────────────────┐  |
|  | 1. Combien font 7 + 8 ?                    → 15             |  |
|  | 2. Combien font 12 × 3 ?                   → 36             |  |
|  | 3. Combien font 100 ÷ 4 ?                  → 25             |  |
|  └────────────────────────────────────────────────────────────┘  |
|  ...                                                              |
|                                                                   |
|  [Modifier]                                    [Supprimer]        |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/additions/{id}/` | [api-reference](../../../backend/api-reference.md) §2.5 |

---

## 3 - AdditionCreatePage / AdditionEditPage

### Principe

Page dédiée pour créer/modifier une manche Addition. Utilise `<AdditionForm />` avec les questions en `<AdditionQuestionInlineForm />`. Chaque question a un énoncé et une réponse courte.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer une manche Addition  (ou Modifier)                         |
+------------------------------------------------------------------+
|                                                                   |
|  <AdditionForm />                                                 |
|                                                                   |
|  Titre *      [________________________________________________]  |
|  Description  [________________________________________________]  |
|  Original     [ ] Cette manche est originale                      |
|                                                                   |
|  Questions (type AD, 8 par défaut)                                |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ <AdditionQuestionInlineForm />                              │  |
|  │ # | Énoncé                      | Réponse courte |         │  |
|  │ 1 | [________________________]  | [__________]   | [🗑]    │  |
|  │   | [✓ Sauvegardée]                              | [Valider]│  |
|  ├────────────────────────────────────────────────────────────┤  |
|  │ 2 | [________________________]  | [__________]   | [🗑]    │  |
|  │   | [⏳ Non sauvée]                              | [Valider]│  |
|  └────────────────────────────────────────────────────────────┘  |
|  ... (jusqu'à 8 ou plus)                                          |
|                                                                   |
|  [+ Ajouter une question]                                         |
|                                                                   |
|  [Annuler]                                      [Enregistrer]     |
+------------------------------------------------------------------+
```

### Appels API

| Action                           | Méthode   | Endpoint                                | Réf.                                                    |
| -------------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                            | POST      | `/api/quiz/additions/`                  | [api-reference](../../../backend/api-reference.md) §2.5 |
| Modifier                         | PUT/PATCH | `/api/quiz/additions/{id}/`             | idem                                                    |
| Questions (liste pour sélection) | GET       | `/api/quiz/questions/?question_type=AD` | §2.1                                                    |

---

## 4 - AdditionForm (modale)

### Principe

Formulaire utilisé dans une modale depuis `BurgerQuizDetailEdit` pour créer ou éditer une manche Addition directement attachée au quiz.

### Wireframe (dans modale)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Créer une manche Addition                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <AdditionForm />                                                    │
│                                                                      │
│  Titre *      [________________________________________________]     │
│  Description  [________________________________________________]     │
│  Original     [ ] Cette manche est originale                         │
│                                                                      │
│  Questions (type AD)                                                 │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ <AdditionQuestionInlineForm />                              │     │
│  │ 1. Énoncé [______________________]  Réponse [________]      │     │
│  │    [✓ Sauvegardée]                              [🗑]        │     │
│  │    [Valider]                                                │     │
│  ├────────────────────────────────────────────────────────────┤     │
│  │ 2. Énoncé [______________________]  Réponse [________]      │     │
│  │    [⏳ Non sauvée]                              [🗑]        │     │
│  │    [Valider]                                                │     │
│  └────────────────────────────────────────────────────────────┘     │
│  ...                                                                 │
│                                                                      │
│  [+ Ajouter une question]                                            │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]     │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux

```
<AdditionModal /> (depuis BurgerQuizDetailEdit)
     │
     ▼
<AdditionForm />
     │
     ├── Saisie titre, description, original
     │
     ├── Ajout de questions
     │     │
     │     └── <AdditionQuestionInlineForm />
     │           ├── Saisie énoncé + réponse courte
     │           ├── [Valider] → sauvegarde locale
     │           └── Statut affiché (✓ | ⏳ | ⚠️)
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
[[POST /api/quiz/additions/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { addition_id: newId }
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

## 5 - AdditionQuestionInlineForm

### Principe

Composant inline pour saisir une question Addition avec un énoncé et une **réponse courte**. Inclut un bouton **Valider** pour confirmer la question et un **statut de sauvegarde**.

### Props

```typescript
interface AdditionQuestionInlineFormProps {
  question?: AdditionQuestion; // Question existante (édition)
  index: number; // Position dans la liste
  onSave: (data: AdditionQuestionData) => void;
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
│  Énoncé *         [________________________________________________]
│                                                                  │
│  Réponse courte * [________________]                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Statut : ✓ Sauvegardée                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Valider]                                              [🗑]     │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe compact (dans tableau)

```
┌──────────────────────────────────────────────────────────────────┐
│ # | Énoncé                      | Réponse courte |               │
│ 1 | [________________________]  | [__________]   | [🗑]          │
│   | [✓ Sauvegardée]                              | [Valider]     │
└──────────────────────────────────────────────────────────────────┘
```

### Flux de validation

```
<AdditionQuestionInlineForm />
     │
     ├── Statut initial: 📝 Nouvelle
     │
     ▼
(Saisie énoncé + réponse courte)
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
     │   • "La réponse est requise"
     │
     └── ✅ Valide
              │
              ▼
         Statut: ✓ Sauvegardée (vert)
         Données stockées localement
         (envoi API au submit du formulaire parent)
```

### Validation

| Champ          | Règle                      |
| -------------- | -------------------------- |
| Énoncé         | Requis, min 10 caractères  |
| Réponse courte | Requis, max 100 caractères |

---

## Appels API récapitulatifs

| Action                         | Méthode | Endpoint                                | Réf. |
| ------------------------------ | ------- | --------------------------------------- | ---- |
| Lister manches                 | GET     | `/api/quiz/additions/`                  | §2.5 |
| Détail manche                  | GET     | `/api/quiz/additions/{id}/`             | §2.5 |
| Créer manche                   | POST    | `/api/quiz/additions/`                  | §2.5 |
| Modifier manche                | PATCH   | `/api/quiz/additions/{id}/`             | §2.5 |
| Supprimer manche               | DELETE  | `/api/quiz/additions/{id}/`             | §2.5 |
| Rechercher questions (type AD) | GET     | `/api/quiz/questions/?question_type=AD` | §2.1 |
