# Flux Quiz

Flux de gestion des Burger Quiz et de leurs manches.

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                       QUIZ FLOW                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Dashboard → BurgerQuizList → BurgerQuizDetailEdit              │
│                  ↓                                               │
│             BurgerQuizCreate                                     │
│                  ↓                                               │
│             BurgerQuizDetailEdit (création + gestion manches)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Liste des Burger Quiz

### Flux

```
[BurgerQuizListPage]
     │
     ▼
[[GET /api/burger-quiz/]]
     │
     ▼
{Données reçues}
     │
     ├── Liste vide → Afficher "Aucun quiz" + Bouton créer
     │
     └── Liste → Afficher cards (titre, date, preview manches)
                    │
                    ├── (Clic card) → [BurgerQuizDetailEdit]
                    └── (Clic "Supprimer") → Modal confirmation
```

### Endpoints

| Action    | Method | Endpoint                | Params                         |
| --------- | ------ | ----------------------- | ------------------------------ |
| Liste     | GET    | `/api/burger-quiz/`     | `?page=1&ordering=-created_at` |
| Supprimer | DELETE | `/api/burger-quiz/:id/` | —                              |

### TanStack Query

```typescript
// src/features/burger-quiz/hooks/useQuizList.ts

export function useQuizList(page = 1) {
  return useQuery({
    queryKey: ["burger-quiz", "list", page],
    queryFn: () => quizApi.getList(page),
  });
}

export function useDeleteQuiz() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: quizApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["burger-quiz"] });
      toast.success("Quiz supprimé");
    },
  });
}
```

---

## 2. Création d'un Burger Quiz

### Flux

```
[BurgerQuizCreatePage]
     │
     ▼
<BurgerQuizForm />
     │
     ├── Champs obligatoires :
     │     • titre (requis)
     │     • toss (requis)
     │     • tags (optionnel)
     │
     ▼
[[POST /api/burger-quiz/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   redirect → [BurgerQuizDetailEdit] + toast "Quiz créé"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs de validation (par champ, inline)
```

### Endpoints

| Action | Method | Endpoint            | Body                     | Response     |
| ------ | ------ | ------------------- | ------------------------ | ------------ |
| Créer  | POST   | `/api/burger-quiz/` | `{ title, toss, tags? }` | `BurgerQuiz` |

### Données requises

```typescript
interface BurgerQuizCreateInput {
  title: string; // Obligatoire
  toss: string; // Obligatoire
  tags?: string[]; // Optionnel
}
```

### TanStack Query

```typescript
// src/features/burger-quiz/hooks/useCreateQuiz.ts

export function useCreateQuiz() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: quizApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["burger-quiz"] });
      toast.success("Quiz créé");
      navigate(`/quiz/${data.id}`);
    },
    onError: (error) => {
      // Erreurs gérées par le formulaire (validation inline)
    },
  });
}
```

---

## 3. BurgerQuizDetailEdit (Détail + Édition)

Page unique combinant détail et édition du quiz et de ses manches.

### Flux principal

```
[BurgerQuizDetailEdit]
     │
     ▼
[[GET /api/burger-quiz/:id/]]
     │
     ▼
Afficher :
├── <BurgerQuizDetailCard />
│     ├── Titre, toss, tags (lecture seule)
│     └── Bouton [✏️ Modifier] → switch vers <BurgerQuizForm />
│
├── <BurgerQuizForm /> (si mode édition)
│     ├── Édition titre, toss, tags
│     ├── [Annuler] → retour BurgerQuizDetailCard
│     └── [Enregistrer] → PATCH + retour BurgerQuizDetailCard
│
└── <RoundStructure />
      ├── Nuggets        → [Créer] | [Attacher] | [Éditer] | [Détacher]
      ├── Sel ou Poivre  → [Créer] | [Attacher] | [Éditer] | [Détacher]
      ├── Menus          → [Créer] | [Attacher] | [Éditer] | [Détacher]
      ├── Addition       → [Créer] | [Attacher] | [Éditer] | [Détacher]
      └── Burger de mort → [Créer] | [Attacher] | [Éditer] | [Détacher]
```

### Flux édition infos quiz

```
<BurgerQuizDetailCard />
     │
     ▼
(Clic "Modifier")
     │
     ▼
<BurgerQuizForm /> (pré-rempli)
     │
     ▼
(Modifier titre, toss, tags)
     │
     ▼
[[PATCH /api/burger-quiz/:id/]]
     │
     ├── ✅ 200 OK
     │        │
     │        ▼
     │   Retour <BurgerQuizDetailCard /> + toast "Quiz modifié"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs (inline par champ)
```

### Endpoints

| Action          | Method | Endpoint                | Body                       | Response     |
| --------------- | ------ | ----------------------- | -------------------------- | ------------ |
| Charger         | GET    | `/api/burger-quiz/:id/` | —                          | `BurgerQuiz` |
| Modifier infos  | PATCH  | `/api/burger-quiz/:id/` | `{ title?, toss?, tags? }` | `BurgerQuiz` |
| Attacher manche | PATCH  | `/api/burger-quiz/:id/` | `{ nuggets_id: 123 }`      | `BurgerQuiz` |
| Détacher manche | PATCH  | `/api/burger-quiz/:id/` | `{ nuggets_id: null }`     | `BurgerQuiz` |
| Supprimer quiz  | DELETE | `/api/burger-quiz/:id/` | —                          | —            |

### Indicateurs de complétion des manches

```typescript
interface RoundStatus {
  id: string | null;
  name: string;
  isComplete: boolean;
  questionCount: number;
  minQuestions: number;
}

// Exemple d'état
{
  nuggets: { id: "123", isComplete: true, questionCount: 8, minQuestions: 4 },
  saltOrPepper: { id: null, isComplete: false, questionCount: 0, minQuestions: 5 },
  menus: { id: "456", isComplete: false, questionCount: 2, minQuestions: 3 },
  addition: { id: "789", isComplete: true, questionCount: 8, minQuestions: 8 },
  deadlyBurger: { id: null, isComplete: false, questionCount: 0, minQuestions: 10 },
}
```

---

## 4. Gestion des Manches (RoundStructure)

### Flux — Créer une manche

```
<RoundSlot /> (slot vide)
     │
     ▼
(Clic "Créer")
     │
     ▼
<NuggetsModal /> (ou autre selon le type)
     │
     ▼
<NuggetsForm />
     ├── Titre, original
     └── Questions via <NuggetsQuestionInlineForm />
           │
           ├── Saisie question + réponses
           ├── [Valider] → sauvegarde individuelle
           └── Statut : ✓ Sauvegardée | ⏳ Non sauvée | ⚠️ Erreur
     │
     ▼
[[POST /api/nuggets/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { nuggets_id: newId }
     │        │
     │        ▼
     │   Fermer modale + refresh RoundStructure
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs dans le formulaire
```

### Flux — Attacher une manche existante

```
<RoundSlot /> (slot vide)
     │
     ▼
(Clic "Attacher")
     │
     ▼
<SearchAndSelectNuggets /> (ou autre selon le type)
     │
     ├── Recherche : [________] 🔍
     │
     ├── Résultats :
     │     ○ Culture générale (6 questions)
     │     ● Sciences & Nature (4 questions) ✓
     │
     ▼
(Sélection + clic "Attacher")
     │
     ▼
[[PATCH /api/burger-quiz/:id/]] { nuggets_id: selectedId }
     │
     ├── ✅ 200 OK
     │        │
     │        ▼
     │   Fermer modale + refresh RoundStructure
     │
     └── ❌ Error
              │
              ▼
         toast erreur
```

### Flux — Éditer une manche

```
<RoundSlot /> (slot rempli)
     │
     ▼
(Clic "Éditer")
     │
     ▼
<NuggetsModal /> (mode édition)
     │
     ▼
[[GET /api/nuggets/:id/]]
     │
     ▼
<NuggetsForm /> (pré-rempli)
     │
     ▼
(Modifications)
     │
     ▼
[[PATCH /api/nuggets/:id/]]
     │
     ├── ✅ 200 OK → Fermer modale + refresh
     │
     └── ❌ 400 → Afficher erreurs
```

### Flux — Détacher une manche

```
<RoundSlot /> (slot rempli)
     │
     ▼
(Clic "Détacher")
     │
     ▼
Modal confirmation : "Détacher cette manche ?"
     │
     ├── (Annuler) → Fermer
     │
     └── (Confirmer)
              │
              ▼
         [[PATCH /api/burger-quiz/:id/]] { nuggets_id: null }
              │
              ▼
         Refresh RoundStructure
```

### Endpoints par manche

| Manche            | List                       | Create | Detail      | Update        | Delete         |
| ----------------- | -------------------------- | ------ | ----------- | ------------- | -------------- |
| Nuggets           | GET `/api/nuggets/`        | POST   | GET `/:id/` | PATCH `/:id/` | DELETE `/:id/` |
| Sel ou Poivre     | GET `/api/salt-or-pepper/` | POST   | GET `/:id/` | PATCH `/:id/` | DELETE `/:id/` |
| Menus             | GET `/api/menus/`          | POST   | GET `/:id/` | PATCH `/:id/` | DELETE `/:id/` |
| Addition          | GET `/api/addition/`       | POST   | GET `/:id/` | PATCH `/:id/` | DELETE `/:id/` |
| Burger de la mort | GET `/api/deadly-burger/`  | POST   | GET `/:id/` | PATCH `/:id/` | DELETE `/:id/` |

---

## 5. Gestion des Questions (InlineForm)

### Pattern InlineForm avec statut de sauvegarde

Chaque question dans un formulaire de manche utilise un composant `InlineForm` dédié qui gère :

- La saisie des données
- La sauvegarde individuelle
- L'affichage du statut

```typescript
interface QuestionInlineFormState {
  isDirty: boolean; // Modifications non sauvegardées
  isSaved: boolean; // Sauvegardée avec succès
  isSubmitting: boolean; // En cours de sauvegarde
  errors: FieldErrors; // Erreurs de validation
}

type SaveStatus = "new" | "dirty" | "saving" | "saved" | "error";
```

### Composants par type de manche

| Manche            | InlineForm                                                | Particularité                       |
| ----------------- | --------------------------------------------------------- | ----------------------------------- |
| Nuggets           | `<NuggetsQuestionInlineForm />`                           | Par paires, 4 réponses + correcte   |
| Sel ou Poivre     | `<SaltOrPepperQuestionInlineForm />`                      | Réponse = dropdown des propositions |
| Menus             | `<MenuThemeInlineForm />` + `<MenusQuestionInlineForm />` | 3 slots de thèmes (2 CL + 1 TR)     |
| Addition          | `<AdditionQuestionInlineForm />`                          | Énoncé + réponse courte             |
| Burger de la mort | `<DeadlyBurgerQuestionInlineForm />`                      | Énoncé seul (pas de réponse)        |

> **Note Menus** : La manche Menus a une structure imbriquée. Le `<MenusForm />` contient 3 slots pour des `MenuTheme`. Chaque slot permet d'**attacher** un thème existant ou de **créer** un nouveau thème via `<MenuThemeInlineForm />`. Les questions sont gérées au niveau du thème via `<MenusQuestionInlineForm />`.

### Flux — Ajouter une question (InlineForm)

```
<NuggetsForm />
     │
     ▼
(Clic "+ Ajouter une paire")
     │
     ▼
Ajout de 2x <NuggetsQuestionInlineForm />
     │
     ├── Saisie question 1 + 4 réponses + correcte
     │        │
     │        ▼
     │   (Clic "Valider")
     │        │
     │        ▼
     │   Statut: ⏳ → Sauvegarde... → ✓ Sauvegardée
     │
     └── Saisie question 2...
```

### Flux — Valider une question

```
<NuggetsQuestionInlineForm />
     │
     ├── Statut initial: 📝 Nouvelle
     │
     ▼
(Saisie des données)
     │
     ├── Statut: ⏳ Non sauvegardée (dirty)
     │
     ▼
(Clic "Valider")
     │
     ▼
{Validation locale}
     │
     ├── ❌ Erreur validation → Afficher erreurs inline
     │
     └── ✅ Valide
              │
              ▼
         Statut: ⏳ Sauvegarde en cours...
              │
              ▼
         (Appel API optionnel ou stockage local)
              │
              ├── ✅ Succès → Statut: ✓ Sauvegardée (vert)
              │
              └── ❌ Erreur → Statut: ⚠️ Erreur (rouge)
```

### Affichage des statuts

```typescript
const statusConfig = {
  new: { icon: "📝", text: "Nouvelle", color: "gray" },
  dirty: { icon: "⏳", text: "Non sauvegardée", color: "yellow" },
  saving: { icon: "⏳", text: "Sauvegarde...", color: "blue" },
  saved: { icon: "✓", text: "Sauvegardée", color: "green" },
  error: { icon: "⚠️", text: "Erreur", color: "red" },
};
```

---

## 6. TanStack Query — Hooks

```typescript
// src/features/burger-quiz/hooks/index.ts

// === Quiz ===
export function useQuizList(page?: number);
export function useQuiz(id: string);
export function useCreateQuiz();
export function useUpdateQuiz();
export function useDeleteQuiz();

// === Manches ===
export function useNuggetsList(params?: { search?: string });
export function useNuggets(id: string);
export function useCreateNuggets();
export function useUpdateNuggets();

export function useSaltPepperList(params?: { search?: string });
export function useSaltPepper(id: string);
export function useCreateSaltPepper();
export function useUpdateSaltPepper();

// ... idem pour Menus, Addition, DeadlyBurger

// === Attachement ===
export function useAttachRound(quizId: string);
export function useDetachRound(quizId: string);
```

---

## 7. Cache et Invalidation

```typescript
// Query Keys
const quizKeys = {
  all: ["burger-quiz"] as const,
  lists: () => [...quizKeys.all, "list"] as const,
  list: (page: number) => [...quizKeys.lists(), page] as const,
  details: () => [...quizKeys.all, "detail"] as const,
  detail: (id: string) => [...quizKeys.details(), id] as const,
};

const nuggetsKeys = {
  all: ["nuggets"] as const,
  lists: () => [...nuggetsKeys.all, "list"] as const,
  list: (params?: object) => [...nuggetsKeys.lists(), params] as const,
  details: () => [...nuggetsKeys.all, "detail"] as const,
  detail: (id: string) => [...nuggetsKeys.details(), id] as const,
};

// Invalidation après mutation
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: quizKeys.detail(quizId) });
};
```

---

## 8. Arborescence des Composants

```
src/features/burger-quiz/
├── pages/
│   ├── BurgerQuizListPage.tsx
│   ├── BurgerQuizCreatePage.tsx
│   └── BurgerQuizDetailEdit.tsx
│
├── components/
│   ├── BurgerQuizForm.tsx
│   ├── BQDetailCard.tsx
│   ├── RoundStructure.tsx
│   │
│   ├── rounds/
│   │   ├── RoundSlot.tsx
│   │   ├── NuggetsForm.tsx
│   │   ├── NuggetsModal.tsx
│   │   ├── SaltOrPepperForm.tsx
│   │   ├── SaltOrPepperModal.tsx
│   │   ├── MenusForm.tsx              # Contient 3 slots de MenuTheme
│   │   ├── MenusModal.tsx
│   │   ├── MenuThemeSlot.tsx          # Slot pour un thème (CL ou TR)
│   │   ├── MenuThemeInlineForm.tsx    # Création inline d'un thème
│   │   ├── AdditionForm.tsx
│   │   ├── AdditionModal.tsx
│   │   ├── DeadlyBurgerForm.tsx
│   │   └── DeadlyBurgerModal.tsx
│   │
│   ├── questions/
│   │   ├── NuggetsQuestionInlineForm.tsx
│   │   ├── SaltOrPepperQuestionInlineForm.tsx
│   │   ├── MenusQuestionInlineForm.tsx    # Utilisé dans MenuThemeInlineForm
│   │   ├── AdditionQuestionInlineForm.tsx
│   │   └── DeadlyBurgerQuestionInlineForm.tsx
│   │
│   └── search/
│       ├── SearchAndSelectNuggets.tsx
│       ├── SearchAndSelectSaltOrPepper.tsx
│       ├── SearchAndSelectMenus.tsx
│       ├── SearchAndSelectMenuTheme.tsx   # Recherche thème (filtre CL/TR)
│       ├── SearchAndSelectAddition.tsx
│       └── SearchAndSelectDeadlyBurger.tsx
│
└── hooks/
    ├── useQuizList.ts
    ├── useQuiz.ts
    ├── useCreateQuiz.ts
    ├── useUpdateQuiz.ts
    ├── useDeleteQuiz.ts
    ├── useAttachRound.ts
    ├── useDetachRound.ts
    ├── useMenuThemeList.ts
    ├── useCreateMenuTheme.ts
    └── ... (hooks par manche)
```

---

## Récapitulatif des pages Quiz

| Page                 | Route          | Description                         |
| -------------------- | -------------- | ----------------------------------- |
| BurgerQuizListPage   | `/quiz`        | Liste des quiz                      |
| BurgerQuizCreatePage | `/quiz/create` | Créer un quiz (formulaire simple)   |
| BurgerQuizDetailEdit | `/quiz/:id`    | Détail + Édition du quiz et manches |

> **Note** : La route `/quiz/:id/edit` est supprimée car fusionnée dans `/quiz/:id`.
