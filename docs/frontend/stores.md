# États Globaux (Stores)

Définition des états globaux pour le frontend avec **Zustand**.

**Fichier cible** : `src/features/*/store.ts` ou `src/stores/`

---

## Vue d'ensemble

| Store                   | Librairie | Persistance  | Description                  |
| ----------------------- | --------- | ------------ | ---------------------------- |
| `useAuthStore`          | Zustand   | localStorage | Authentification utilisateur |
| `useThemeStore`         | Zustand   | localStorage | Thème dark/light (prévu)     |
| `useQuizStructureStore` | Zustand   | Non          | Structure du quiz en édition |
| `useGameStore`          | Zustand   | Non          | Session de jeu en cours      |

> **Note d'architecture**
>
> - Les **stores transverses** (auth, thème) vivent dans `src/store/`.
> - Les **stores métier** (quiz, play, etc.) vivent dans leurs dossiers de feature (`src/features/*/store.ts`).
> - Les **notifications** sont gérées via les **toasts `shadcn/ui`** (`useToast` + `<Toaster />`), sans store Zustand dédié.

---

## 1. AuthStore

Gestion de l'authentification utilisateur.

> **Note** : Les tokens JWT sont gérés séparément dans `tokenStorage` (voir [Gestion des tokens](#gestion-des-tokens)).

```typescript
// src/stores/auth.ts

import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import type { User } from "@/types/auth";

interface AuthState {
  // State
  user: User | null;
  isAuthenticated: boolean;
  isHydrated: boolean;

  // Actions
  setUser: (user: User | null) => void;
  login: (user: User) => void;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
  setHydrated: (hydrated: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isHydrated: false,

      // Actions
      setUser: (user) =>
        set({
          user,
          isAuthenticated: !!user,
        }),

      login: (user) =>
        set({
          user,
          isAuthenticated: true,
        }),

      logout: () =>
        set({
          user: null,
          isAuthenticated: false,
        }),

      updateUser: (data) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...data } : null,
        })),

      setHydrated: (isHydrated) => set({ isHydrated }),
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        state?.setHydrated(true);
      },
    },
  ),
);

// Selectors (pour optimiser les re-renders)
export const selectUser = (state: AuthState) => state.user;
export const selectIsAuthenticated = (state: AuthState) =>
  state.isAuthenticated;
export const selectIsHydrated = (state: AuthState) => state.isHydrated;
```

### Données stockées

| Propriété         | Type           | Persisté           | Description                                   |
| ----------------- | -------------- | ------------------ | --------------------------------------------- |
| `user`            | `User \| null` | Oui (localStorage) | Utilisateur connecté                          |
| `isAuthenticated` | `boolean`      | Oui (localStorage) | État de connexion                             |
| `isHydrated`      | `boolean`      | Non                | `true` quand le store a fini de se réhydrater |

### Qu'est-ce que `isHydrated` ?

Zustand persist charge les données depuis localStorage de manière **asynchrone**. Pendant ce court laps de temps, le state est dans son état initial (`user: null`), ce qui peut causer un "flash" où l'app pense que l'utilisateur n'est pas connecté.

`isHydrated` permet d'attendre que la réhydratation soit terminée avant d'afficher le contenu protégé :

```tsx
// Exemple dans ProtectedRoute
const isHydrated = useAuthStore(selectIsHydrated);
const isAuthenticated = useAuthStore(selectIsAuthenticated);

if (!isHydrated) {
  return <LoadingSpinner />;
}

if (!isAuthenticated) {
  return <Navigate to="/login" />;
}
```

---

### Gestion des tokens

Les tokens JWT sont gérés **séparément** dans `src/lib/axios.ts` via `tokenStorage` :

```typescript
// src/lib/axios.ts

const TOKEN_KEYS = {
  access: "access_token",
  refresh: "refresh_token",
} as const;

export const tokenStorage = {
  getAccess: () => localStorage.getItem(TOKEN_KEYS.access),
  getRefresh: () => localStorage.getItem(TOKEN_KEYS.refresh),
  setTokens: (access: string, refresh: string) => {
    localStorage.setItem(TOKEN_KEYS.access, access);
    localStorage.setItem(TOKEN_KEYS.refresh, refresh);
  },
  setAccess: (access: string) => {
    localStorage.setItem(TOKEN_KEYS.access, access);
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEYS.access);
    localStorage.removeItem(TOKEN_KEYS.refresh);
  },
};
```

**Pourquoi cette séparation ?**

1. **Couplage HTTP** : Les tokens sont injectés automatiquement via les interceptors axios
2. **Refresh automatique** : La logique de refresh 401 est gérée au même endroit
3. **Simplicité** : Le store auth reste focalisé sur les données utilisateur

---

## 2. ThemeStore

Gestion du thème clair/sombre.

```typescript
// src/stores/theme.ts

import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark" | "system";

interface ThemeState {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      theme: "system",

      setTheme: (theme) => set({ theme }),

      toggleTheme: () =>
        set((state) => ({
          theme: state.theme === "dark" ? "light" : "dark",
        })),
    }),
    {
      name: "theme-storage",
    },
  ),
);
```

### Intégration shadcn/ui

```typescript
// src/providers (ThemeProvider)

import { useEffect } from "react";
import { useThemeStore } from "@/stores/theme";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { theme } = useThemeStore();

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("light", "dark");

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
      root.classList.add(systemTheme);
    } else {
      root.classList.add(theme);
    }
  }, [theme]);

  return <>{children}</>;
}
```

---

## 3. Notifications (shadcn / toasts)

> **Décision :** pas de `NotificationStore` Zustand.  
> Les notifications sont gérées uniquement via les **toasts `shadcn/ui`**.

### Principe

- Utilisation de `components/ui/use-toast.ts` :
  - Hook `useToast()` pour déclencher des toasts.
  - Composant global `<Toaster />` monté une seule fois (dans les providers / layout).
- Les toasts sont **éphémères** et ne sont pas stockés dans un store global.
- Les mutations React Query (create/edit/delete) appellent `toast({ title, description, variant })`
  directement dans les hooks / composants.

### Bonnes pratiques

- Centraliser éventuellement 1–2 helpers dans `lib/notifications.ts` (ex. `showSuccessToast`, `showErrorToast`)
  qui wrappe `useToast` pour uniformiser le wording et les variantes.

---

## 4. QuizStructureStore

Gestion de la structure ordonnée d'un Burger Quiz en édition.

```typescript
// src/features/quiz/store.ts

import { create } from "zustand";
import {
  BurgerQuizElement,
  BurgerQuizElementInput,
} from "@/types/burger-quiz-element";
import { VideoInterludeRef } from "@/types/video-interlude";

interface QuizStructureState {
  // State
  quizId: string | null;
  elements: BurgerQuizElement[];
  isDirty: boolean;
  isSaving: boolean;

  // Actions
  setQuizId: (id: string | null) => void;
  setElements: (elements: BurgerQuizElement[]) => void;
  reorderElement: (fromIndex: number, toIndex: number) => void;
  addInterlude: (interlude: VideoInterludeRef, atIndex?: number) => void;
  removeInterlude: (index: number) => void;
  markDirty: () => void;
  markClean: () => void;
  setSaving: (saving: boolean) => void;
  reset: () => void;
}

const initialState = {
  quizId: null,
  elements: [],
  isDirty: false,
  isSaving: false,
};

export const useQuizStructureStore = create<QuizStructureState>((set, get) => ({
  ...initialState,

  setQuizId: (quizId) => set({ quizId }),

  setElements: (elements) => set({ elements, isDirty: false }),

  reorderElement: (fromIndex, toIndex) =>
    set((state) => {
      const newElements = [...state.elements];
      const [removed] = newElements.splice(fromIndex, 1);
      newElements.splice(toIndex, 0, removed);
      // Recalculer les ordres
      return {
        elements: newElements.map((el, i) => ({ ...el, order: i })),
        isDirty: true,
      };
    }),

  addInterlude: (interlude, atIndex) =>
    set((state) => {
      const newElement: BurgerQuizElement = {
        order: atIndex ?? state.elements.length,
        element_type: "interlude",
        interlude,
      };
      const newElements = [...state.elements];
      if (atIndex !== undefined) {
        newElements.splice(atIndex, 0, newElement);
      } else {
        newElements.push(newElement);
      }
      // Recalculer les ordres
      return {
        elements: newElements.map((el, i) => ({ ...el, order: i })),
        isDirty: true,
      };
    }),

  removeInterlude: (index) =>
    set((state) => {
      const element = state.elements[index];
      if (element?.element_type !== "interlude") return state;
      const newElements = state.elements.filter((_, i) => i !== index);
      return {
        elements: newElements.map((el, i) => ({ ...el, order: i })),
        isDirty: true,
      };
    }),

  markDirty: () => set({ isDirty: true }),
  markClean: () => set({ isDirty: false }),
  setSaving: (isSaving) => set({ isSaving }),
  reset: () => set(initialState),
}));
```

### Données du QuizStructureStore

| Propriété  | Type                  | Description                    |
| ---------- | --------------------- | ------------------------------ |
| `quizId`   | `string \| null`      | ID du quiz en cours d'édition  |
| `elements` | `BurgerQuizElement[]` | Structure ordonnée             |
| `isDirty`  | `boolean`             | Modifications non sauvegardées |
| `isSaving` | `boolean`             | Sauvegarde en cours            |

---

## 5. GameStore 🚧

Gestion de la session de jeu en cours (Play).

```typescript
// src/features/play/store.ts

import { create } from "zustand";
import { GameSession, Player, Team } from "@/types/session";
import { QuestionDetail } from "@/types/quiz";

type GamePhase =
  | "lobby"
  | "toss"
  | "nuggets"
  | "salt_or_pepper"
  | "menus"
  | "addition"
  | "deadly_burger"
  | "results";

interface GameState {
  // Session
  session: GameSession | null;
  currentPlayer: Player | null;

  // Game progress
  phase: GamePhase;
  currentQuestion: QuestionDetail | null;
  currentQuestionIndex: number;
  timer: number;
  isTimerRunning: boolean;

  // Scores
  scores: {
    ketchup: number;
    mayo: number;
  };

  // Actions - Session
  setSession: (session: GameSession | null) => void;
  setCurrentPlayer: (player: Player | null) => void;
  updatePlayer: (playerId: string, data: Partial<Player>) => void;

  // Actions - Game
  setPhase: (phase: GamePhase) => void;
  setCurrentQuestion: (question: QuestionDetail | null, index?: number) => void;
  nextQuestion: () => void;

  // Actions - Timer
  setTimer: (seconds: number) => void;
  startTimer: () => void;
  stopTimer: () => void;
  decrementTimer: () => void;

  // Actions - Score
  addScore: (team: Team, points: number) => void;
  resetScores: () => void;

  // Reset
  reset: () => void;
}

const initialState = {
  session: null,
  currentPlayer: null,
  phase: "lobby" as GamePhase,
  currentQuestion: null,
  currentQuestionIndex: 0,
  timer: 0,
  isTimerRunning: false,
  scores: { ketchup: 0, mayo: 0 },
};

export const useGameStore = create<GameState>((set, get) => ({
  ...initialState,

  // Session
  setSession: (session) => set({ session }),
  setCurrentPlayer: (currentPlayer) => set({ currentPlayer }),
  updatePlayer: (playerId, data) =>
    set((state) => ({
      session: state.session
        ? {
            ...state.session,
            players: state.session.players.map((p) =>
              p.id === playerId ? { ...p, ...data } : p,
            ),
          }
        : null,
    })),

  // Game
  setPhase: (phase) => set({ phase }),
  setCurrentQuestion: (currentQuestion, index) =>
    set({
      currentQuestion,
      currentQuestionIndex: index ?? get().currentQuestionIndex,
    }),
  nextQuestion: () =>
    set((state) => ({
      currentQuestionIndex: state.currentQuestionIndex + 1,
    })),

  // Timer
  setTimer: (timer) => set({ timer }),
  startTimer: () => set({ isTimerRunning: true }),
  stopTimer: () => set({ isTimerRunning: false }),
  decrementTimer: () =>
    set((state) => ({
      timer: Math.max(0, state.timer - 1),
    })),

  // Score
  addScore: (team, points) =>
    set((state) => ({
      scores: {
        ...state.scores,
        [team]: state.scores[team] + points,
      },
    })),
  resetScores: () => set({ scores: { ketchup: 0, mayo: 0 } }),

  // Reset
  reset: () => set(initialState),
}));
```

### Données du GameStore

| Propriété              | Type                     | Description           |
| ---------------------- | ------------------------ | --------------------- |
| `session`              | `GameSession \| null`    | Session active        |
| `currentPlayer`        | `Player \| null`         | Joueur local          |
| `phase`                | `GamePhase`              | Phase de jeu actuelle |
| `currentQuestion`      | `QuestionDetail \| null` | Question affichée     |
| `currentQuestionIndex` | `number`                 | Index dans la manche  |
| `timer`                | `number`                 | Secondes restantes    |
| `isTimerRunning`       | `boolean`                | Timer actif           |
| `scores`               | `{ ketchup, mayo }`      | Scores des équipes    |

---

## Organisation des fichiers

```
src/
├── store/
│   ├── index.ts          # Re-exports (useAuthStore, selectors...)
│   └── authStore.ts      # useAuthStore (user, isAuthenticated, isHydrated)
│
└── features/
    ├── quiz/
    │   └── store.ts      # useQuizStructureStore (à venir)
    │
    └── play/
        └── store.ts      # useGameStore (à venir)
```

> **Note** : Le store auth vit dans `src/store/authStore.ts`, pas dans `features/auth`.  
> Les stores métier (quiz, play) sont dans leur feature.

---

## Alternatives considérées

| Solution       | Avantages                                           | Inconvénients           |
| -------------- | --------------------------------------------------- | ----------------------- |
| **Zustand** ✅ | Simple, léger, TypeScript natif, middleware persist | —                       |
| Context API    | Natif React, pas de dépendance                      | Verbeux, re-renders     |
| Redux Toolkit  | Robuste, DevTools                                   | Complexe pour ce projet |
| Jotai          | Atomique, simple                                    | Moins de middleware     |

**Choix : Zustand** pour sa simplicité et sa bonne intégration TypeScript.
