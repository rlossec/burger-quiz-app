# Wireframes — Burger Quiz

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [BurgerQuizListPage](#1-burgerquizlistpage)
- [BurgerQuizCreatePage](#2-burgerquizcreatepage)
- [BurgerQuizDetailEdit](#3-burgerquizdetailedit)

---

## 1 - BurgerQuizListPage

### Principe

Liste des Burger Quiz : titre, date/création, **une colonne par manche** (Nuggets, Sel ou Poivre, Menus, Addition, Burger de la mort). Chaque manche affiche un **état** : **complet** (manche renseignée et valide), **partiel** (manche en cours ou incomplète), **absente** (aucune manche choisie). Bouton Créer. Actions : détail, suppression.

### Wireframe

```
+-----------------------------------------------------------------------+
|  Burger Quiz                                           [ + Créer ]    |
+-----------------------------------------------------------------------+
|  Titre          | Date       | NU | SP | ME | AD | BdM | Actions      |
|-----------------|------------|----|----|----|----|-----|--------------|
|  Soirée PCaT #1 | 15/02/2025 | ✅ | ✅ | ✏️| ✏️ | ✏️  | [✏️][🗑]      |
|  Quiz test      | 10/02/2025 | 🚫 | 🚫 | 🚫| 🚫 | 🚫  | [✏️][🗑]      |
+-----------------------------------------------------------------------+
```

### Appels API

| Action    | Méthode | Endpoint                         | Réf.                                                    |
| --------- | ------- | -------------------------------- | ------------------------------------------------------- |
| Lister    | GET     | `/api/quiz/burger-quizzes/`      | [api-reference](../../../backend/api-reference.md) §2.7 |
| Supprimer | DELETE  | `/api/quiz/burger-quizzes/{id}/` | idem                                                    |

---

## 2 - BurgerQuizCreatePage

### Principe

Page de création d'un Burger Quiz avec formulaire simple. Champs obligatoires uniquement. Après création réussie, redirection vers `BurgerQuizDetailEdit`.

### Composant principal

**`<BurgerQuizForm />`** — Formulaire de création/édition des infos de base.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer un Burger Quiz                                            |
+------------------------------------------------------------------+
|  <BurgerQuizForm />                                              |
|                                                                  |
|  Titre *  [________________________________________________]     |
|           ⚠️ Le titre est obligatoire                            |
|                                                                  |
|  Toss *   [________________________________________________]     |
|           ⚠️ Le toss est obligatoire                             |
|                                                                  |
|  Tags     [________________________________________________]     |
|           (séparés par des virgules)                             |
|                                                                  |
|  ( Annuler )                                    ( Créer )        |
+------------------------------------------------------------------+
```

### Flux

```
[BurgerQuizCreatePage]
     │
     ▼
(Saisie titre, toss, tags)
     │
     ▼
[[POST /api/quiz/burger-quizzes/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   redirect → [BurgerQuizDetailEdit] + toast "Quiz créé"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs par champ (inline)
```

### Appels API

| Action | Méthode | Endpoint                    | Body                    | Response     |
| ------ | ------- | --------------------------- | ----------------------- | ------------ |
| Créer  | POST    | `/api/quiz/burger-quizzes/` | `{ title, toss, tags }` | `BurgerQuiz` |

---

## 3 - BurgerQuizDetailEdit

### Principe

Page **unique** combinant détail et édition d'un Burger Quiz. Trois sections principales :

1. **`<BurgerQuizDetailCard />`** — Affichage des infos (titre, toss, tags) avec bouton pour passer en mode édition (`<BurgerQuizForm />`)
2. **`<RoundStructure />`** — Structure des 5 manches avec actions Créer/Attacher pour chaque slot
3. **`<QuizStructureEditor />`** — Structure ordonnée du quiz (manches + interludes) avec drag & drop

### Wireframe complet

```
┌─────────────────────────────────────────────────────────────────────┐
│  Burger Quiz — Soirée PCaT #1                          [🗑 Supprimer]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  <BurgerQuizDetailCard />                  [✏️ Modifier]    │    │
│  │                                                             │    │
│  │  Titre : Soirée PCaT #1                                     │    │
│  │  Toss  : Bienvenue dans le Burger Quiz !                    │    │
│  │  Tags  : #culture #cinema #musique                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ─────────── (clic sur Modifier) ───────────                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  <BurgerQuizForm />  (mode édition)                         │    │
│  │                                                             │    │
│  │  Titre * [Soirée PCaT #1_________________________]          │    │
│  │  Toss  * [Bienvenue dans le Burger Quiz !________]          │    │
│  │  Tags    [#culture, #cinema, #musique____________]          │    │
│  │                                                             │    │
│  │  [Annuler]                              [Enregistrer]       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  <RoundStructure />                                                 │
│  Structure des manches                                              │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ < NuggetsForm />                                             │   │
│  │ 🍗 Nuggets                                                   │   │
│  │ [✅ Culture G (6 questions)]               [✏️] [🔗] [🗑️]   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ <SaltOrPepperForm/>                                          │   │
│  │ 🧂 Sel ou Poivre                                             │   │
│  │ [✅ Noir ou Blanc (5 questions)]           [✏️] [🔗] [🗑️]   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ <MenusForm/>                                                 │   │
│  │ 🍽️ Menus                                                     │   │
│  │ [⏳ Menus du jour (2/3 thèmes)]            [✏️] [🔗] [🗑️]   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ <AdditionForm/>                                              │   │
│  │ ➕ Addition                                                  │   │
│  │ [✅ Addition rapide (8 questions)]         [✏️] [🔗] [🗑️]   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ <DeadlyBurgerForm/>                                          │   │
│  │ 🍔 Burger de la mort                                         │   │
│  │                                                              │   │
│  │ [✅ Finale épique (10 questions)]          [✏️] [🔗] [🗑️]   │   │
│  │                                                              │   │
│  │ — OU si vide —                                               │   │
│  │                                                              │   │
│  │ [Aucune manche]                  [+ Créer]  [🔗 Attacher]    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  <QuizStructureEditor />                                            │
│  Structure ordonnée (drag & drop)                    [+ Interlude]  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 1. 🎬 Intro Burger Quiz (Interlude)              [⋮] [🗑️]   │   │
│  │ 2. 🍗 Nuggets — Culture G                        [⋮] [—]    │   │
│  │ 3. 📺 Pub Sponsor (Interlude)                    [⋮] [🗑️]   │   │
│  │ 4. 🧂 Sel ou Poivre — Noir ou Blanc              [⋮] [—]    │   │
│  │ 5. 🍽️ Menus — Menus du jour                      [⋮] [—]    │   │
│  │ 6. 📺 Pub 2 (Interlude)                          [⋮] [🗑️]   │   │
│  │ 7. ➕ Addition — Addition rapide                 [⋮] [—]    │   │
│  │ 8. 🍔 Burger de la mort — Finale épique          [⋮] [—]    │   │
│  │ 9. 🎬 Outro Credits (Interlude)                  [⋮] [🗑️]   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ℹ️ Glissez-déposez pour réorganiser. Les manches sont obligatoires,│
│     les interludes sont optionnels et peuvent être supprimés.       │
│                                                                     │
│  [Enregistrer la structure]                                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Composants

#### `<BurgerQuizDetailCard />`

Affichage en lecture seule des informations du quiz.

| Prop   | Type       | Description                     |
| ------ | ---------- | ------------------------------- |
| quiz   | BurgerQuiz | Données du quiz                 |
| onEdit | () => void | Callback pour passer en édition |

#### `<BurgerQuizForm />`

Formulaire d'édition des infos de base.

| Prop          | Type                    | Description                       |
| ------------- | ----------------------- | --------------------------------- |
| quiz?         | BurgerQuiz              | Données existantes (mode édition) |
| onSubmit      | (data) => Promise<void> | Callback de soumission            |
| onCancel?     | () => void              | Callback d'annulation             |
| isSubmitting? | boolean                 | État de chargement                |

#### `<RoundStructure />`

Conteneur des 5 slots de manches.

| Prop     | Type       | Description                 |
| -------- | ---------- | --------------------------- |
| quiz     | BurgerQuiz | Quiz avec ses manches       |
| onUpdate | () => void | Callback après modification |

#### `<RoundSlot />`

Slot individuel pour une manche (générique).

| Prop      | Type          | Description                             |
| --------- | ------------- | --------------------------------------- |
| roundType | RoundType     | Type de manche (nuggets, saltPepper...) |
| round     | Round \| null | Manche attachée ou null                 |
| onCreate  | () => void    | Ouvre modale de création                |
| onAttach  | () => void    | Ouvre modale de recherche               |
| onEdit    | () => void    | Ouvre modale d'édition                  |
| onDetach  | () => void    | Détache la manche du quiz               |

#### `<QuizStructureEditor />`

Éditeur drag & drop de la structure ordonnée du quiz.

| Prop       | Type                | Description            |
| ---------- | ------------------- | ---------------------- |
| quizId     | string              | ID du Burger Quiz      |
| structure  | BurgerQuizElement[] | Structure actuelle     |
| onSave     | (elements) => void  | Callback de sauvegarde |
| isLoading? | boolean             | État de chargement     |

#### `<StructureElement />`

Élément individuel dans la structure (manche ou interlude).

| Prop        | Type              | Description                         |
| ----------- | ----------------- | ----------------------------------- |
| element     | BurgerQuizElement | Données de l'élément                |
| index       | number            | Position dans la liste              |
| isDragging? | boolean           | État de drag                        |
| onRemove?   | () => void        | Suppression (interludes uniquement) |

#### `<AddInterludeButton />`

Bouton pour ajouter un interlude à la structure.

| Prop      | Type                | Description                            |
| --------- | ------------------- | -------------------------------------- |
| onSelect  | (interlude) => void | Callback quand un interlude est choisi |
| position? | number              | Position d'insertion souhaitée         |

---

## 4 - Modales de Création de Manche

Chaque type de manche a sa propre modale avec formulaire dédié.

### Actions disponibles par slot

| État du slot | Actions disponibles                          |
| ------------ | -------------------------------------------- |
| Vide         | `[+ Créer]` `[🔗 Attacher]`                  |
| Rempli       | `[✏️ Éditer]` `[🔗 Changer]` `[🗑️ Détacher]` |

### Modales de création

| Manche            | Composant Modal         | Formulaire             |
| ----------------- | ----------------------- | ---------------------- |
| Nuggets           | `<NuggetsModal />`      | `<NuggetsForm />`      |
| Sel ou Poivre     | `<SaltOrPepperModal />` | `<SaltOrPepperForm />` |
| Menus             | `<MenusModal />`        | `<MenusForm />`        |
| Addition          | `<AdditionModal />`     | `<AdditionForm />`     |
| Burger de la mort | `<DeadlyBurgerModal />` | `<DeadlyBurgerForm />` |

### Wireframe modale création (exemple Nuggets)

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
│  │ Paire 1                                                     │     │
│  │ <NuggetsQuestionInlineForm />  <NuggetsQuestionInlineForm />│     │
│  │ [Q1: ____________]             [Q2: ____________]           │     │
│  │ [R1-R4 + correcte]             [R1-R4 + correcte]           │     │
│  │ [✓ Sauvegardée]                [⏳ Non sauvée]             │     │
│  │ [Valider]                      [Valider]                    │     │
│  └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  [+ Ajouter une paire de questions]                                  │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5 - Modales de Recherche et Sélection

Pour attacher une manche existante au quiz.

### Composants de recherche

| Manche            | Composant                         |
| ----------------- | --------------------------------- |
| Nuggets           | `<SearchAndSelectNuggets />`      |
| Sel ou Poivre     | `<SearchAndSelectSaltOrPepper />` |
| Menus             | `<SearchAndSelectMenus />`        |
| Addition          | `<SearchAndSelectAddition />`     |
| Burger de la mort | `<SearchAndSelectDeadlyBurger />` |

### Wireframe modale recherche

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Attacher une manche Nuggets                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <SearchAndSelectNuggets />                                          │
│                                                                      │
│  Recherche : [_______________________] 🔍                            │
│                                                                      │
│  Résultats :                                                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ○ Culture générale (6 questions) — utilisé 2x                │   │
│  │ ○ Épisode 123 (8 questions) — original                       │   │
│  │ ● Sciences & Nature (4 questions) — sélectionné ✓            │   │
│  │ ○ Histoire (6 questions)                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Attacher]        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6 - Appels API

### Page BurgerQuizDetailEdit

| Action            | Méthode | Endpoint                                   | Body / Params                |
| ----------------- | ------- | ------------------------------------------ | ---------------------------- |
| Charger quiz      | GET     | `/api/quiz/burger-quizzes/{id}/`           | —                            |
| Modifier infos    | PATCH   | `/api/quiz/burger-quizzes/{id}/`           | `{ title?, toss?, tags? }`   |
| Attacher manche   | PATCH   | `/api/quiz/burger-quizzes/{id}/`           | `{ nuggets_id: 123 }` (ex.)  |
| Détacher manche   | PATCH   | `/api/quiz/burger-quizzes/{id}/`           | `{ nuggets_id: null }` (ex.) |
| Supprimer quiz    | DELETE  | `/api/quiz/burger-quizzes/{id}/`           | —                            |
| Charger structure | GET     | `/api/quiz/burger-quizzes/{id}/structure/` | —                            |
| Sauver structure  | PUT     | `/api/quiz/burger-quizzes/{id}/structure/` | `{ elements: [...] }`        |

### Structure (BurgerQuizElement)

| Champ        | Type    | Description                                       |
| ------------ | ------- | ------------------------------------------------- |
| element_type | string  | `"round"` ou `"interlude"`                        |
| round_type   | string? | `"NU"`, `"SP"`, `"ME"`, `"AD"`, `"DB"` (si round) |
| interlude_id | string? | UUID de l'interlude (si interlude)                |

### Exemple de payload structure

```json
{
  "elements": [
    { "element_type": "interlude", "interlude_id": "uuid-intro" },
    { "element_type": "round", "round_type": "NU" },
    { "element_type": "interlude", "interlude_id": "uuid-pub1" },
    { "element_type": "round", "round_type": "SP" },
    { "element_type": "round", "round_type": "ME" },
    { "element_type": "interlude", "interlude_id": "uuid-pub2" },
    { "element_type": "round", "round_type": "AD" },
    { "element_type": "round", "round_type": "DB" },
    { "element_type": "interlude", "interlude_id": "uuid-outro" }
  ]
}
```

### Modales de création

| Manche            | Méthode | Endpoint                    |
| ----------------- | ------- | --------------------------- |
| Nuggets           | POST    | `/api/quiz/nuggets/`        |
| Sel ou Poivre     | POST    | `/api/quiz/salt-or-pepper/` |
| Menus             | POST    | `/api/quiz/menus/`          |
| Addition          | POST    | `/api/quiz/additions/`      |
| Burger de la mort | POST    | `/api/quiz/deadly-burgers/` |

### Modales de recherche

| Manche            | Méthode | Endpoint                    | Params        |
| ----------------- | ------- | --------------------------- | ------------- |
| Nuggets           | GET     | `/api/quiz/nuggets/`        | `?search=...` |
| Sel ou Poivre     | GET     | `/api/quiz/salt-or-pepper/` | `?search=...` |
| Menus             | GET     | `/api/quiz/menus/`          | `?search=...` |
| Addition          | GET     | `/api/quiz/additions/`      | `?search=...` |
| Burger de la mort | GET     | `/api/quiz/deadly-burgers/` | `?search=...` |
