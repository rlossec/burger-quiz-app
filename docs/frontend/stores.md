# États Globaux (Stores)

Définition des états globaux pour le frontend avec **Zustand**.

**Fichier cible** : `src/features/*/store.ts` ou `src/stores/`

---

## Vue d'ensemble

| Store                    | Librairie | Persistance  | Description                     |
| ------------------------ | --------- | ------------ | ------------------------------- |
| `useAuthStore`           | Zustand   | localStorage | Authentification utilisateur    |
| `useThemeStore`          | Zustand   | localStorage | Thème dark/light                |
| `useNotificationStore`   | Zustand   | Non          | Toasts et alertes               |
| `useQuizStructureStore`  | Zustand   | Non          | Structure du quiz en édition    |
| `useGameStore`           | Zustand   | Non          | Session de jeu en cours         |

---

## 1. AuthStore

Gestion de l'authentification utilisateur.

```typescript
// src/features/auth/store.ts

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { User, AuthTokens } from "@/types/auth";

interface AuthState {
  // State
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  setTokens: (tokens: AuthTokens | null) => void;
  login: (user: User, tokens: AuthTokens) => void;
  logout: () => void;
  updateUser: (data: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: true,

      // Actions
      setUser: (user) => set({ user, isAuthenticated: !!user }),

      setTokens: (tokens) => set({ tokens }),

      login: (user, tokens) =>
        set({ user, tokens, isAuthenticated: true, isLoading: false }),

      logout: () => set({ user: null, tokens: null, isAuthenticated: false }),

      updateUser: (data) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...data } : null,
        })),
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        tokens: state.tokens,
      }),
    },
  ),
);
```

### Données stockées

| Propriété         | Type                 | Persisté           | Description             |
| ----------------- | -------------------- | ------------------ | ----------------------- |
| `user`            | `User \| null`       | Non                | Utilisateur connecté    |
| `tokens`          | `AuthTokens \| null` | Oui (localStorage) | Access + Refresh tokens |
| `isAuthenticated` | `boolean`            | Non                | Calculé depuis user     |
| `isLoading`       | `boolean`            | Non                | Chargement initial      |

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
// src/app/providers.tsx

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

## 3. NotificationStore

Gestion des notifications toast.

```typescript
// src/stores/notification.ts

import { create } from "zustand";

type NotificationType = "success" | "error" | "warning" | "info";

interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number; // ms, défaut 5000
}

interface NotificationState {
  notifications: Notification[];
  add: (notification: Omit<Notification, "id">) => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],

  add: (notification) =>
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id: crypto.randomUUID() },
      ],
    })),

  remove: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),

  clear: () => set({ notifications: [] }),
}));

// Helper functions
export const toast = {
  success: (title: string, message?: string) =>
    useNotificationStore.getState().add({ type: "success", title, message }),
  error: (title: string, message?: string) =>
    useNotificationStore.getState().add({ type: "error", title, message }),
  warning: (title: string, message?: string) =>
    useNotificationStore.getState().add({ type: "warning", title, message }),
  info: (title: string, message?: string) =>
    useNotificationStore.getState().add({ type: "info", title, message }),
};
```

---

## 4. QuizStructureStore

Gestion de la structure ordonnée d'un Burger Quiz en édition.

```typescript
// src/features/quiz/store.ts

import { create } from "zustand";
import { BurgerQuizElement, BurgerQuizElementInput } from "@/types/burger-quiz-element";
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

| Propriété  | Type                  | Description                              |
| ---------- | --------------------- | ---------------------------------------- |
| `quizId`   | `string \| null`      | ID du quiz en cours d'édition            |
| `elements` | `BurgerQuizElement[]` | Structure ordonnée                       |
| `isDirty`  | `boolean`             | Modifications non sauvegardées           |
| `isSaving` | `boolean`             | Sauvegarde en cours                      |

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

| Propriété              | Type                  | Description           |
| ---------------------- | --------------------- | --------------------- |
| `session`              | `GameSession \| null` | Session active        |
| `currentPlayer`        | `Player \| null`      | Joueur local          |
| `phase`                | `GamePhase`           | Phase de jeu actuelle |
| `currentQuestion`      | `QuestionDetail \| null` | Question affichée  |
| `currentQuestionIndex` | `number`              | Index dans la manche  |
| `timer`                | `number`              | Secondes restantes    |
| `isTimerRunning`       | `boolean`             | Timer actif           |
| `scores`               | `{ ketchup, mayo }`   | Scores des équipes    |

---

## Organisation des fichiers

```
src/
├── stores/
│   ├── index.ts          # Re-exports
│   ├── theme.ts
│   └── notification.ts
│
└── features/
    ├── auth/
    │   └── store.ts      # useAuthStore
    │
    ├── quiz/
    │   └── store.ts      # useQuizStructureStore
    │
    └── play/
        └── store.ts      # useGameStore
```

---

## Alternatives considérées

| Solution       | Avantages                                           | Inconvénients           |
| -------------- | --------------------------------------------------- | ----------------------- |
| **Zustand** ✅ | Simple, léger, TypeScript natif, middleware persist | —                       |
| Context API    | Natif React, pas de dépendance                      | Verbeux, re-renders     |
| Redux Toolkit  | Robuste, DevTools                                   | Complexe pour ce projet |
| Jotai          | Atomique, simple                                    | Moins de middleware     |

**Choix : Zustand** pour sa simplicité et sa bonne intégration TypeScript.
