# Wireframes — Sel ou Poivre

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [SaltOrPepperListPage](#1-saltorpepperlistpage)
- [SaltOrPepperDetailPage](#2-saltorpepperdetailpage)
- [SaltOrPepperCreatePage / SaltOrPepperEditPage](#3-saltorpeppercreatepage--saltorpeppereditpage)
- [SaltOrPepperForm (modale depuis BurgerQuizDetailEdit)](#4-saltorpepperform-modale)
- [SaltOrPepperQuestionInlineForm](#5-saltorpepperquestioninlineform)

---

## 1 - SaltOrPepperListPage

### Principe

Liste des manches Sel ou poivre : colonnes titre, original ?, nombre d'utilisation, nombre de questions. Bouton Ajouter → SaltOrPepperCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Sel ou Poivre                        [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Titre               | Original ? | Utilisations | Nbre Q | Actions   |
|----------------------|------------|--------------|--------|-----------|
|  Noir ou Blanc       | oui        | 2            | 5      | [👁][✏️][🗑] |
|  Vrai ou Faux        | non        | 1            | 8      | [👁][✏️][🗑] |
|  ...                 | ...        | ...          | ...    | ...       |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/salt-or-pepper/` | [api-reference](../../../backend/api-reference.md) §2.3 |

---

## 2 - SaltOrPepperDetailPage

### Principe

Affichage en lecture : titre, description, original ?, propositions (choice_labels), liste des questions avec la réponse correcte pour chacune. Actions : SaltOrPepperEditPage, suppression (modale).

### Wireframe

```
+-------------------------------------------------------------------+
|  Manche Sel ou Poivre — Noir ou Blanc                              |
+-------------------------------------------------------------------+
|  Titre        : Noir ou Blanc                                      |
|  Description  : Questions sur les couleurs et nuances              |
|  Original     : oui                                                |
|                                                                    |
|  Propositions : Noir | Blanc | Les deux                           |
|                                                                    |
|  Questions (5) :                                                   |
|  ┌────────────────────────────────────────────────────────────────┐|
|  | 1. Le corbeau est de quelle couleur ?         → Noir           ||
|  | 2. La neige est de quelle couleur ?           → Blanc          ||
|  | 3. Le zèbre a quelles couleurs ?              → Les deux       ||
|  └────────────────────────────────────────────────────────────────┘|
|  ...                                                               |
|                                                                    |
|  [Modifier]                                       [Supprimer]      |
+-------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                         | Réf.                                                    |
| ------ | ------- | -------------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/salt-or-pepper/{id}/` | [api-reference](../../../backend/api-reference.md) §2.3 |

---

## 3 - SaltOrPepperCreatePage / SaltOrPepperEditPage

### Principe

Page dédiée pour créer/modifier une manche Sel ou Poivre. Les **propositions** (2 à 5) définissent les choix possibles pour toutes les questions. Chaque question utilise un `<SaltOrPepperQuestionInlineForm />` avec un dropdown lié aux propositions.

### Wireframe

```
+----------------------------------------------------------------------+
|  Créer une manche Sel ou Poivre  (ou Modifier)                        |
+----------------------------------------------------------------------+
|                                                                       |
|  <SaltOrPepperForm />                                                 |
|                                                                       |
|  Titre *      [________________________________________________]      |
|  Description  [________________________________________________]      |
|  Original     [ ] Cette manche est originale                          |
|                                                                       |
|  Propositions (2 à 5 choix) *                                         |
|  [ Noir ] [ Blanc ] [ Les deux ] [+] [−]                              |
|                                                                       |
|  Questions                                                            |
|  ┌──────────────────────────────────────────────────────────────────┐|
|  │ <SaltOrPepperQuestionInlineForm />                                ||
|  │ Énoncé [________________________________]  Réponse [ Noir ▼ ]     ||
|  │ [✓ Sauvegardée]                                           [🗑]   ||
|  │ [Valider]                                                         ||
|  ├──────────────────────────────────────────────────────────────────┤|
|  │ <SaltOrPepperQuestionInlineForm />                                ||
|  │ Énoncé [________________________________]  Réponse [ Blanc ▼ ]    ||
|  │ [⏳ Non sauvée]                                           [🗑]   ||
|  │ [Valider]                                                         ||
|  └──────────────────────────────────────────────────────────────────┘|
|                                                                       |
|  [+ Ajouter une question]                                             |
|                                                                       |
|  [Annuler]                                          [Enregistrer]     |
+----------------------------------------------------------------------+
```

### Appels API

| Action                    | Méthode   | Endpoint                                | Réf.                                                    |
| ------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                     | POST      | `/api/quiz/salt-or-pepper/`             | [api-reference](../../../backend/api-reference.md) §2.3 |
| Modifier                  | PUT/PATCH | `/api/quiz/salt-or-pepper/{id}/`        | idem                                                    |
| Questions (liste type SP) | GET       | `/api/quiz/questions/?question_type=SP` | §2.1                                                    |

---

## 4 - SaltOrPepperForm (modale)

### Principe

Formulaire utilisé dans une modale depuis `BurgerQuizDetailEdit` pour créer ou éditer une manche Sel ou Poivre directement attachée au quiz.

### Wireframe (dans modale)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Créer une manche Sel ou Poivre                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <SaltOrPepperForm />                                                │
│                                                                      │
│  Titre *      [________________________________________________]     │
│  Description  [________________________________________________]     │
│  Original     [ ] Cette manche est originale                         │
│                                                                      │
│  Propositions (2 à 5 choix) *                                        │
│  [ Noir ] [ Blanc ] [ Les deux ] [+] [−]                             │
│                                                                      │
│  Questions                                                           │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ <SaltOrPepperQuestionInlineForm />                          │     │
│  │ Énoncé [____________________________]  Réponse [ Noir ▼ ]   │     │
│  │ [✓ Sauvegardée]                                      [🗑]   │     │
│  │ [Valider]                                                   │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  [+ Ajouter une question]                                            │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]     │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux

```
<SaltOrPepperModal /> (depuis BurgerQuizDetailEdit)
     │
     ▼
<SaltOrPepperForm />
     │
     ├── Saisie titre, description, original
     │
     ├── Définition des propositions (2-5)
     │     │
     │     └── Les propositions alimentent le dropdown des questions
     │
     ├── Ajout de questions
     │     │
     │     └── <SaltOrPepperQuestionInlineForm />
     │           ├── Saisie énoncé
     │           ├── Sélection réponse (dropdown des propositions)
     │           ├── [Valider] → sauvegarde locale
     │           └── Statut affiché (✓ | ⏳ | ⚠️)
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
[[POST /api/quiz/salt-or-pepper/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { salt_or_pepper_id: newId }
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

## 5 - SaltOrPepperQuestionInlineForm

### Principe

Composant inline pour saisir une question Sel ou Poivre. La réponse est un **dropdown** alimenté par les propositions définies dans le formulaire parent. Inclut un bouton **Valider** et un **statut de sauvegarde**.

### Props

```typescript
interface SaltOrPepperQuestionInlineFormProps {
  question?: SaltOrPepperQuestion;   // Question existante (édition)
  choices: string[];                 // Propositions du formulaire parent
  onSave: (data: SaltOrPepperQuestionData) => void;
  onRemove?: () => void;
}
```

### États de sauvegarde

| Statut   | Icône | Description                | Couleur |
| -------- | ----- | -------------------------- | ------- |
| `new`    | 📝    | Nouvelle question          | Gris    |
| `dirty`  | ⏳    | Non sauvegardée            | Jaune   |
| `saving` | ⏳    | Sauvegarde en cours        | Bleu    |
| `saved`  | ✓     | Sauvegardée                | Vert    |
| `error`  | ⚠️    | Erreur de validation/save  | Rouge   |

### Wireframe détaillé

```
┌─────────────────────────────────────────────────────────────────┐
│  Question 1                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Énoncé *  [________________________________________________]    │
│                                                                  │
│  Réponse * [ Noir           ▼ ]                                 │
│            ┌─────────────────┐                                  │
│            │ Noir            │                                  │
│            │ Blanc           │                                  │
│            │ Les deux        │                                  │
│            └─────────────────┘                                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Statut : ✓ Sauvegardée                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Valider]                                              [🗑]     │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe compact (dans liste)

```
┌──────────────────────────────────────────────────────────────────┐
│ Énoncé [________________________________]  Réponse [ Noir ▼ ]    │
│ [✓ Sauvegardée]                                          [🗑]   │
│ [Valider]                                                        │
└──────────────────────────────────────────────────────────────────┘
```

### Flux de validation

```
<SaltOrPepperQuestionInlineForm />
     │
     ├── Statut initial: 📝 Nouvelle
     │
     ▼
(Saisie énoncé + sélection réponse)
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

### Comportement spécial : synchronisation avec les propositions

```
{Modification des propositions dans le formulaire parent}
     │
     ▼
{Pour chaque question existante}
     │
     ├── Réponse toujours valide → Pas de changement
     │
     └── Réponse supprimée des propositions
              │
              ▼
         Statut: ⚠️ Erreur
         Message: "La réponse sélectionnée n'existe plus"
         → L'utilisateur doit re-sélectionner une réponse
```

### Validation

| Champ    | Règle                                  |
| -------- | -------------------------------------- |
| Énoncé   | Requis, min 10 caractères              |
| Réponse  | Requis, doit être une des propositions |

---

## Appels API récapitulatifs

| Action                         | Méthode   | Endpoint                                | Réf.  |
| ------------------------------ | --------- | --------------------------------------- | ----- |
| Lister manches                 | GET       | `/api/quiz/salt-or-pepper/`             | §2.3  |
| Détail manche                  | GET       | `/api/quiz/salt-or-pepper/{id}/`        | §2.3  |
| Créer manche                   | POST      | `/api/quiz/salt-or-pepper/`             | §2.3  |
| Modifier manche                | PATCH     | `/api/quiz/salt-or-pepper/{id}/`        | §2.3  |
| Supprimer manche               | DELETE    | `/api/quiz/salt-or-pepper/{id}/`        | §2.3  |
| Rechercher questions (type SP) | GET       | `/api/quiz/questions/?question_type=SP` | §2.1  |
