# Wireframes — Menus + MenuTheme

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [MenuThemeListPage](#1-menuthemelistpage)
- [MenuThemeDetailPage](#2-menuthemedetailpage)
- [MenuThemeCreatePage / MenuThemeEditPage](#3-menuthemecreatepage--menuthemeeditpage)
- [MenusListPage](#4-menuslistpage)
- [MenusDetailPage](#5-menusdetailpage)
- [MenusCreatePage / MenusEditPage](#6-menuscreatepage--menuseditpage)
- [MenusForm (modale depuis BurgerQuizDetailEdit)](#7-menusform-modale)
- [MenuThemeInlineForm](#8-menuthemeinlineform)
- [MenusQuestionInlineForm](#9-menusquestioninlineform)

---

## 1 - MenuThemeListPage

### Principe

Liste des thèmes de menu (MenuTheme) : colonnes titre, type (CL/TR), original ?, nombre d'utilisation, nombre de questions. Bouton Ajouter → MenuThemeCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Thèmes de menu                                [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Type (CL/TR) | Original ? | Utilisations | Nbre Q | Actions   |
|------------------|--------------|------------|--------------|--------|-----------|
|  Gastronomie     | CL           | oui        | 1            | 3      | [👁][✏️][🗑] |
|  Animaux         | CL           | non        | 2            | 4      | [👁][✏️][🗑] |
|  Piège ultime    | TR           | oui        | 1            | 3      | [👁][✏️][🗑] |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                 | Réf.                                                    |
| ------ | ------- | ------------------------ | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/menu-themes/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 2 - MenuThemeDetailPage

### Principe

Détail d'un thème : titre, type (Classique / Troll), original, liste ordonnée des questions. Actions : MenuThemeEditPage, suppression.

### Wireframe

```
+------------------------------------------------------------------+
|  Thème de menu — Gastronomie                                      |
+------------------------------------------------------------------+
|  Titre    : Gastronomie                                           |
|  Type     : Classique (CL)                                        |
|  Original : oui                                                   |
|                                                                   |
|  Questions (3) :                                                  |
|  ┌────────────────────────────────────────────────────────────┐  |
|  | 1. Quel est le plat national français ?     → Pot-au-feu   |  |
|  | 2. D'où vient le croissant ?                → Autriche     |  |
|  | 3. Combien d'étoiles au maximum Michelin ?  → 3            |  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [Modifier]                                    [Supprimer]        |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                      | Réf.                                                    |
| ------ | ------- | ----------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/menu-themes/{id}/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 3 - MenuThemeCreatePage / MenuThemeEditPage

### Principe

Page dédiée pour créer/modifier un thème de menu. Utilise des `<MenusQuestionInlineForm />` pour les questions.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer un thème de menu  (ou Modifier)                            |
+------------------------------------------------------------------+
|                                                                   |
|  Titre *  [________________________________________________]      |
|  Type *   (•) Classique (CL)   ( ) Troll (TR)                     |
|  Original [ ] Ce thème est original                               |
|                                                                   |
|  Questions (type ME)                                              |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ <MenusQuestionInlineForm />                                 │  |
|  │ 1. Énoncé [____________________]  Réponse [________]        │  |
|  │    [✓ Sauvegardée]                              [🗑]        │  |
|  │    [Valider]                                                │  |
|  ├────────────────────────────────────────────────────────────┤  |
|  │ 2. Énoncé [____________________]  Réponse [________]        │  |
|  │    [⏳ Non sauvée]                              [🗑]        │  |
|  │    [Valider]                                                │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [+ Ajouter une question]                                         |
|                                                                   |
|  [Annuler]                                      [Enregistrer]     |
+------------------------------------------------------------------+
```

### Appels API

| Action                    | Méthode   | Endpoint                                | Réf.                                                    |
| ------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                     | POST      | `/api/quiz/menu-themes/`                | [api-reference](../../../backend/api-reference.md) §2.4 |
| Modifier                  | PUT/PATCH | `/api/quiz/menu-themes/{id}/`           | idem                                                    |
| Questions (liste type ME) | GET       | `/api/quiz/questions/?question_type=ME` | §2.1                                                    |

---

## 4 - MenusListPage

### Principe

Liste des manches Menus : colonnes titre, original ?, nombre d'utilisation, statut des 3 thèmes. Bouton Ajouter → MenusCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Menus                                [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | CL1 | CL2 | TR | Actions   |
|------------------|------------|--------------|-----|-----|-----|-----------|
|  Menus du jour   | oui        | 2            | ✅  | ✅  | ✅  | [👁][✏️][🗑] |
|  Menus culture   | non        | 1            | ✅  | ⏳  | 🚫  | [👁][✏️][🗑] |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint           | Réf.                                                    |
| ------ | ------- | ------------------ | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/menus/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 5 - MenusDetailPage

### Principe

Affichage : titre, description, les 3 thèmes (menu 1, menu 2, menu troll) avec pour chacun titre, type et liste des questions. Actions : MenusEditPage, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manche Menus — Menus du jour                                     |
+------------------------------------------------------------------+
|  Titre       : Menus du jour                                      |
|  Description : Trois menus variés pour la soirée                  |
|  Original    : oui                                                |
|                                                                   |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ Menu 1 (Classique) — Gastronomie                            │  |
|  │ 1. Quel est le plat national français ?     → Pot-au-feu   │  |
|  │ 2. D'où vient le croissant ?                → Autriche     │  |
|  │ 3. Combien d'étoiles au maximum Michelin ?  → 3            │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ Menu 2 (Classique) — Animaux                                │  |
|  │ 1. Quel est le plus grand mammifère ?       → Baleine bleue│  |
|  │ 2. ...                                                      │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ Menu Troll — Piège ultime                                   │  |
|  │ 1. Question piège 1...                      → Réponse      │  |
|  │ 2. ...                                                      │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [Modifier]                                    [Supprimer]        |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                | Réf.                                                    |
| ------ | ------- | ----------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/menus/{id}/` | [api-reference](../../../backend/api-reference.md) §2.4 |

---

## 6 - MenusCreatePage / MenusEditPage

### Principe

Page dédiée pour créer/modifier une manche Menus. Contient **3 slots de MenuTheme** :

- 2 slots Classique (CL)
- 1 slot Troll (TR)

Chaque slot permet soit d'**attacher** un thème existant, soit de **créer** un nouveau thème via `<MenuThemeInlineForm />`.

### Wireframe

```
+----------------------------------------------------------------------+
|  Créer une manche Menus  (ou Modifier)                                |
+----------------------------------------------------------------------+
|                                                                       |
|  Titre *      [________________________________________________]      |
|  Description  [________________________________________________]      |
|  Original     [ ] Cette manche est originale                          |
|                                                                       |
|  ════════════════════════════════════════════════════════════════    |
|  Menu 1 (Classique)                                                   |
|  ┌──────────────────────────────────────────────────────────────────┐|
|  │ [✅ Gastronomie (3 questions)]              [✏️] [🔗] [🗑️]       ||
|  │                                                                   ||
|  │ — OU si vide —                                                    ||
|  │                                                                   ||
|  │ [Aucun thème]                     [+ Créer]  [🔗 Attacher]        ||
|  └──────────────────────────────────────────────────────────────────┘|
|                                                                       |
|  ════════════════════════════════════════════════════════════════    |
|  Menu 2 (Classique)                                                   |
|  ┌──────────────────────────────────────────────────────────────────┐|
|  │ <MenuThemeInlineForm type="CL" />  (création inline)              ||
|  │                                                                   ||
|  │ Titre [____________________]                                      ||
|  │ Questions:                                                        ||
|  │   1. [________________] → [________]  [✓] [Valider]              ||
|  │   2. [________________] → [________]  [⏳] [Valider]              ||
|  │ [+ Ajouter question]                                              ||
|  │                                                                   ||
|  │ [Annuler création]                         [Valider le thème]     ||
|  └──────────────────────────────────────────────────────────────────┘|
|                                                                       |
|  ════════════════════════════════════════════════════════════════    |
|  Menu Troll                                                           |
|  ┌──────────────────────────────────────────────────────────────────┐|
|  │ [Aucun thème]                     [+ Créer]  [🔗 Attacher]        ||
|  └──────────────────────────────────────────────────────────────────┘|
|                                                                       |
|  [Annuler]                                          [Enregistrer]     |
+----------------------------------------------------------------------+
```

### Appels API

| Action                        | Méthode   | Endpoint                         | Réf.                                                    |
| ----------------------------- | --------- | -------------------------------- | ------------------------------------------------------- |
| Créer manche                  | POST      | `/api/quiz/menus/`               | [api-reference](../../../backend/api-reference.md) §2.4 |
| Modifier manche               | PUT/PATCH | `/api/quiz/menus/{id}/`          | idem                                                    |
| Liste thèmes (pour recherche) | GET       | `/api/quiz/menu-themes/?type=CL` | idem                                                    |
| Créer thème (inline)          | POST      | `/api/quiz/menu-themes/`         | idem                                                    |

---

## 7 - MenusForm (modale)

### Principe

Formulaire utilisé dans une modale depuis `BurgerQuizDetailEdit` pour créer ou éditer une manche Menus directement attachée au quiz. Contient les **3 slots de MenuTheme** avec les mêmes options que la page dédiée.

### Wireframe (dans modale)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Créer une manche Menus                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <MenusForm />                                                       │
│                                                                      │
│  Titre *      [________________________________________________]     │
│  Description  [________________________________________________]     │
│  Original     [ ] Cette manche est originale                         │
│                                                                      │
│  ══════════════════════════════════════════════════════════════     │
│  Menu 1 (Classique)                                                  │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ [✅ Gastronomie (3 questions)]           [✏️] [🔗] [🗑️]    │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ══════════════════════════════════════════════════════════════     │
│  Menu 2 (Classique)                                                  │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ [Aucun thème]                  [+ Créer]  [🔗 Attacher]     │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ══════════════════════════════════════════════════════════════     │
│  Menu Troll                                                          │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ <MenuThemeInlineForm type="TR" />                           │     │
│  │ Titre [____________________]                                │     │
│  │ Questions:                                                  │     │
│  │   1. [____________] → [______]  [✓] [Valider]              │     │
│  │ [+ Ajouter question]                                        │     │
│  │ [Annuler]                            [Valider le thème]     │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]     │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux

```
<MenusModal /> (depuis BurgerQuizDetailEdit)
     │
     ▼
<MenusForm />
     │
     ├── Saisie titre, description, original
     │
     ├── 3 slots de MenuTheme:
     │     │
     │     ├── Slot Menu 1 (Classique)
     │     │     ├── Option: [🔗 Attacher] → <SearchAndSelectMenuTheme type="CL" />
     │     │     └── Option: [+ Créer] → <MenuThemeInlineForm type="CL" />
     │     │
     │     ├── Slot Menu 2 (Classique)
     │     │     ├── Option: [🔗 Attacher] → <SearchAndSelectMenuTheme type="CL" />
     │     │     └── Option: [+ Créer] → <MenuThemeInlineForm type="CL" />
     │     │
     │     └── Slot Menu Troll
     │           ├── Option: [🔗 Attacher] → <SearchAndSelectMenuTheme type="TR" />
     │           └── Option: [+ Créer] → <MenuThemeInlineForm type="TR" />
     │
     ▼
{Validation: 3 thèmes requis (2 CL + 1 TR)}
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
{Si thèmes créés inline → POST /api/quiz/menu-themes/ pour chaque}
     │
     ▼
[[POST /api/quiz/menus/]] { menu_theme_1_id, menu_theme_2_id, menu_theme_troll_id }
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { menus_id: newId }
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

## 8 - MenuThemeInlineForm

### Principe

Composant inline pour créer un MenuTheme directement dans le formulaire de manche Menus. Contient le titre du thème et ses questions via `<MenusQuestionInlineForm />`. Le **type** (CL ou TR) est déterminé par le slot.

### Props

```typescript
interface MenuThemeInlineFormProps {
  type: "CL" | "TR"; // Type imposé par le slot
  theme?: MenuTheme; // Thème existant (édition)
  onSave: (data: MenuThemeData) => void;
  onCancel: () => void;
}
```

### États de sauvegarde

| Statut   | Icône | Description               | Couleur |
| -------- | ----- | ------------------------- | ------- |
| `new`    | 📝    | Nouveau thème             | Gris    |
| `dirty`  | ⏳    | Non sauvegardé            | Jaune   |
| `saving` | ⏳    | Sauvegarde en cours       | Bleu    |
| `saved`  | ✓     | Sauvegardé                | Vert    |
| `error`  | ⚠️    | Erreur de validation/save | Rouge   |

### Wireframe détaillé

```
┌─────────────────────────────────────────────────────────────────┐
│  Nouveau thème (Classique)                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Titre *  [________________________________________________]     │
│                                                                  │
│  Questions (type ME)                                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ <MenusQuestionInlineForm />                                  ││
│  │ 1. Énoncé [____________________]  Réponse [________]         ││
│  │    [✓ Sauvegardée]                              [🗑]         ││
│  │    [Valider]                                                 ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 2. Énoncé [____________________]  Réponse [________]         ││
│  │    [⏳ Non sauvée]                              [🗑]         ││
│  │    [Valider]                                                 ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [+ Ajouter une question]                                        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Statut thème : ⏳ Non sauvegardé                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  [Annuler]                                [Valider le thème]     │
└─────────────────────────────────────────────────────────────────┘
```

### Flux de validation

```
<MenuThemeInlineForm />
     │
     ├── Statut initial: 📝 Nouveau
     │
     ▼
(Saisie titre + ajout questions)
     │
     ├── Statut: ⏳ Non sauvegardé (dirty)
     │
     ▼
(Clic "Valider le thème")
     │
     ▼
{Validation locale}
     │
     ├── ❌ Erreur
     │        │
     │        ▼
     │   Statut: ⚠️ Erreur + messages
     │   • "Le titre est requis"
     │   • "Au moins 1 question requise"
     │   • "Certaines questions ne sont pas validées"
     │
     └── ✅ Valide (titre + toutes questions saved)
              │
              ▼
         Statut: ✓ Sauvegardé (vert)
         Thème stocké localement
         (création API au submit du formulaire parent)
```

### Validation

| Champ     | Règle                               |
| --------- | ----------------------------------- |
| Titre     | Requis, min 3 caractères            |
| Questions | Au moins 1 requise, toutes validées |

---

## 9 - MenusQuestionInlineForm

### Principe

Composant inline pour saisir une question de type ME (Menus). Énoncé + réponse courte. Utilisé dans `<MenuThemeInlineForm />` et dans les pages de création/édition de thème.

### Props

```typescript
interface MenusQuestionInlineFormProps {
  question?: MenusQuestion; // Question existante (édition)
  index: number; // Position dans la liste
  onSave: (data: MenusQuestionData) => void;
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

### Wireframe compact (dans liste)

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Énoncé [____________________]  Réponse [________]             │
│    [✓ Sauvegardée]                              [🗑]             │
│    [Valider]                                                     │
└──────────────────────────────────────────────────────────────────┘
```

### Validation

| Champ          | Règle                      |
| -------------- | -------------------------- |
| Énoncé         | Requis, min 10 caractères  |
| Réponse courte | Requis, max 100 caractères |

---

## 10 - Modales de recherche MenuTheme

### SearchAndSelectMenuTheme

Permet de rechercher et sélectionner un thème existant pour l'attacher à un slot.

### Wireframe

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Attacher un thème Classique                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <SearchAndSelectMenuTheme type="CL" />                              │
│                                                                      │
│  Recherche : [_______________________] 🔍                            │
│                                                                      │
│  Thèmes disponibles (Classique) :                                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ○ Gastronomie (3 questions) — utilisé 2x                     │   │
│  │ ● Animaux (4 questions) — sélectionné ✓                      │   │
│  │ ○ Géographie (5 questions) — original                        │   │
│  │ ░░ Sciences (3 questions) ░░  ← déjà utilisé dans cette manche│   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Attacher]        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11 - Récapitulatif des composants

### Hiérarchie

```
BurgerQuizDetailEdit
└── RoundStructure
    └── RoundSlot (Menus)
        ├── [Attacher] → SearchAndSelectMenus
        └── [Créer] → MenusModal
                      └── MenusForm
                          ├── Slot Menu 1 (CL)
                          │   ├── [Attacher] → SearchAndSelectMenuTheme
                          │   └── [Créer] → MenuThemeInlineForm
                          │                 └── MenusQuestionInlineForm (×n)
                          ├── Slot Menu 2 (CL)
                          │   └── (idem)
                          └── Slot Menu Troll (TR)
                              └── (idem)
```

### Composants

| Composant                      | Description                                   |
| ------------------------------ | --------------------------------------------- |
| `<MenusForm />`                | Formulaire manche Menus (3 slots)             |
| `<MenuThemeInlineForm />`      | Création inline d'un thème dans un slot       |
| `<MenusQuestionInlineForm />`  | Question type ME avec énoncé + réponse courte |
| `<SearchAndSelectMenus />`     | Recherche manche Menus existante              |
| `<SearchAndSelectMenuTheme />` | Recherche thème existant (filtre CL/TR)       |

---

## Appels API récapitulatifs

| Action                         | Méthode | Endpoint                                | Réf. |
| ------------------------------ | ------- | --------------------------------------- | ---- |
| Lister thèmes                  | GET     | `/api/quiz/menu-themes/`                | §2.4 |
| Lister thèmes (filtre type)    | GET     | `/api/quiz/menu-themes/?type=CL`        | §2.4 |
| Détail thème                   | GET     | `/api/quiz/menu-themes/{id}/`           | §2.4 |
| Créer thème                    | POST    | `/api/quiz/menu-themes/`                | §2.4 |
| Modifier thème                 | PATCH   | `/api/quiz/menu-themes/{id}/`           | §2.4 |
| Supprimer thème                | DELETE  | `/api/quiz/menu-themes/{id}/`           | §2.4 |
| Lister manches Menus           | GET     | `/api/quiz/menus/`                      | §2.4 |
| Détail manche Menus            | GET     | `/api/quiz/menus/{id}/`                 | §2.4 |
| Créer manche Menus             | POST    | `/api/quiz/menus/`                      | §2.4 |
| Modifier manche Menus          | PATCH   | `/api/quiz/menus/{id}/`                 | §2.4 |
| Supprimer manche Menus         | DELETE  | `/api/quiz/menus/{id}/`                 | §2.4 |
| Rechercher questions (type ME) | GET     | `/api/quiz/questions/?question_type=ME` | §2.1 |
