# Types Frontend

Définition des types TypeScript pour le frontend, alignés avec les modèles backend Django.

**Fichier cible** : `src/types/`

---

## Enums

```typescript
export enum QuestionType {
  NU = "NU", // Nuggets
  SP = "SP", // Sel ou Poivre
  ME = "ME", // Menu
  AD = "AD", // Addition
  DB = "DB", // Burger de la Mort
}

export enum MenuThemeType {
  CL = "CL", // Classique
  TR = "TR", // Troll
}

export enum InterludeType {
  IN = "IN", // Intro
  OU = "OU", // Outro
  PU = "PU", // Pub
  IL = "IL", // Interlude générique
}

export enum ElementType {
  ROUND = "round",
  INTERLUDE = "interlude",
}

export type SessionStatus = "waiting" | "playing" | "finished";
export type PlayerRole = "host" | "player" | "spectator";
export type Team = "ketchup" | "mayo";
```

## Generic API wrappers

```typescript
// ─────────────────────────────────────────────
// Generic API wrappers
// ─────────────────────────────────────────────

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}
```

## Auth & User

```typescript
// ── Modèle ──────────────────────────────────

export interface User {
  id: number;
  email: string;
  username: string; // lecture seule
  first_name: string;
  last_name: string;
  avatar?: string;
}

// ── Inputs (formulaires / body) ─────────────

export interface LoginInput {
  username: string;
  password: string;
}

export interface RegisterInput {
  email: string;
  username: string;
  password: string;
  re_password: string;
}

/** PATCH /api/auth/users/me/ ou PATCH /api/auth/users/{id}/ */
export interface UserUpdateInput {
  email?: string;
  first_name?: string;
  last_name?: string;
  avatar?: string;
}

export interface ActivationInput {
  uid: string;
  token: string;
}

export interface ResendActivationInput {
  email: string;
}

export interface ResetPasswordInput {
  email: string;
}

export interface ResetPasswordConfirmInput {
  uid: string;
  token: string;
  new_password: string;
}

export interface RefreshTokenInput {
  refresh: string;
}

export interface VerifyTokenInput {
  token: string;
}

// ── Réponses API ─────────────────────────────

export interface AuthTokens {
  access: string;
  refresh: string;
}
```

---

## Quiz - Éléments de base

```typescript
import { QuestionType } from "./enums";
import { UserRef } from "./auth";

// ─────────────────────────────────────────────
// Auteur (référence légère)
// ─────────────────────────────────────────────

/** Référence légère d'un utilisateur (auteur) */
export interface UserRef {
  id: number;
  username: string;
}

// ─────────────────────────────────────────────
// Answer
// ─────────────────────────────────────────────

export interface Answer {
  id: string; // UUID
  text: string;
  is_correct: boolean;
  image?: string;
}

// ─────────────────────────────────────────────
// Question
// ─────────────────────────────────────────────

/**
 * Question telle que renvoyée dans la liste GET /api/quiz/questions/
 * (sans les réponses)
 */
export interface QuestionList {
  id: string;
  text: string;
  question_type: QuestionType;
  original: boolean;
  explanations?: string;
  video_url?: string;
  image_url?: string;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
}

/**
 * Question telle que renvoyée dans GET /api/quiz/questions/{id}/
 * et dans les détails de manches (avec les réponses)
 */
export interface QuestionDetail extends QuestionList {
  answers: Answer[];
}

// ── Inputs ───────────────────────────────────

export interface AnswerInput {
  text: string;
  is_correct: boolean;
  image?: string;
}

/** POST / PUT /api/quiz/questions/ */
export interface QuestionInput {
  text: string;
  question_type: QuestionType;
  original?: boolean; // défaut true côté API
  explanations?: string;
  video_url?: string;
  image_url?: string;
  answers?: AnswerInput[]; // absent ou [] pour DB
  tags?: string[];
}

/** PATCH /api/quiz/questions/{id}/ */
export type QuestionPatchInput = Partial<QuestionInput>;
```

---

## Burger Quiz

```typescript
import { UserRef } from "./quiz";
import { NuggetsDetail } from "./rounds/nuggets";
import { SaltOrPepperDetail } from "./rounds/salt-or-pepper";
import { MenusDetail } from "./rounds/menus";
import { AdditionDetail } from "./rounds/addition";
import { DeadlyBurgerDetail } from "./rounds/deadly-burger";

// ─────────────────────────────────────────────
// Burger Quiz
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/burger-quizzes/ (liste) */
export interface BurgerQuizList {
  id: string;
  title?: string;
  toss: string;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
}

/**
 * Détail dans GET /api/quiz/burger-quizzes/{id}/
 *
 * Les manches sont exposées avec leur détail complet,
 * incluant toutes leurs questions désérialisées (texte, réponses, etc.).
 * La structure ordonnée inclut les interludes.
 */
export interface BurgerQuizDetail {
  id: string;
  title?: string;
  toss: string;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  nuggets?: NuggetsDetail;
  salt_or_pepper?: SaltOrPepperDetail;
  menus?: MenusDetail;
  addition?: AdditionDetail;
  deadly_burger?: DeadlyBurgerDetail;
  structure: BurgerQuizElement[];
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/burger-quizzes/ et PUT /api/quiz/burger-quizzes/{id}/ */
export interface BurgerQuizInput {
  title?: string;
  toss: string;
  nuggets_id?: string;
  salt_or_pepper_id?: string;
  menus_id?: string;
  addition_id?: string;
  deadly_burger_id?: string;
  tags?: string[];
}

/** PATCH /api/quiz/burger-quizzes/{id}/ */
export type BurgerQuizPatchInput = Partial<BurgerQuizInput>;
```

### Nuggets

```typescript
import { QuestionDetail, UserRef } from "../quiz";

// ─────────────────────────────────────────────
// Manche Nuggets
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/nuggets/ */
export interface NuggetsList {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  burger_quiz_count: number;
}

/**
 * Détail dans GET /api/quiz/nuggets/{id}/
 *
 * Les questions sont désérialisées avec leur contenu complet
 * (texte, réponses, métadonnées).
 */
export interface NuggetsDetail {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  /** Questions complètes avec texte et réponses, ordonnées */
  questions: QuestionDetail[];
  burger_quiz_count: number;
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/nuggets/ et PUT /api/quiz/nuggets/{id}/ */
export interface NuggetsInput {
  title: string;
  original?: boolean;
  question_ids: string[];
  tags?: string[];
}

/** PATCH /api/quiz/nuggets/{id}/ */
export type NuggetsPatchInput = Partial<NuggetsInput>;
```

### Sel ou poivre

```typescript
import { QuestionDetail, UserRef } from "../quiz";

// ─────────────────────────────────────────────
// Manche Sel ou Poivre
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/salt-or-pepper/ */
export interface SaltOrPepperList {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  burger_quiz_count: number;
}

/**
 * Détail dans GET /api/quiz/salt-or-pepper/{id}/
 *
 * Les questions sont désérialisées avec leur contenu complet.
 */
export interface SaltOrPepperDetail {
  id: string;
  title: string;
  description?: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  /** Libellés des propositions, ex: ["Noir", "Blanc", "Les deux"] */
  propositions: string[];
  /** Questions complètes avec texte et réponses, ordonnées */
  questions: QuestionDetail[];
  burger_quiz_count: number;
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/salt-or-pepper/ et PUT /api/quiz/salt-or-pepper/{id}/ */
export interface SaltOrPepperInput {
  title: string;
  description?: string;
  original?: boolean;
  /** 2 à 5 libellés sans doublon */
  propositions: string[];
  question_ids: string[];
  tags?: string[];
}

/** PATCH /api/quiz/salt-or-pepper/{id}/ */
export type SaltOrPepperPatchInput = Partial<SaltOrPepperInput>;
```

### Menus

```typescript
import { MenuThemeType } from "../enums";
import { QuestionDetail, UserRef } from "../quiz";

// ─────────────────────────────────────────────
// MenuTheme
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/menu-themes/ */
export interface MenuThemeList {
  id: string;
  title: string;
  type: MenuThemeType;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  used_in_menus_count: number;
}

/**
 * Détail dans GET /api/quiz/menu-themes/{id}/
 *
 * Les questions sont désérialisées avec leur contenu complet.
 */
export interface MenuThemeDetail {
  id: string;
  title: string;
  type: MenuThemeType;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  /** Questions complètes avec texte et réponses, ordonnées */
  questions: QuestionDetail[];
  used_in_menus_count: number;
}

/** POST /api/quiz/menu-themes/ et PUT /api/quiz/menu-themes/{id}/ */
export interface MenuThemeInput {
  title: string;
  type: MenuThemeType;
  original?: boolean;
  question_ids: string[];
  tags?: string[];
}

/** PATCH /api/quiz/menu-themes/{id}/ */
export type MenuThemePatchInput = Partial<MenuThemeInput>;

// ─────────────────────────────────────────────
// Manche Menus (regroupe 3 MenuTheme)
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/menus/ */
export interface MenusList {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  burger_quiz_count: number;
}

/**
 * Détail dans GET /api/quiz/menus/{id}/
 *
 * Les thèmes sont exposés avec leur détail complet,
 * incluant leurs questions désérialisées.
 */
export interface MenusDetail {
  id: string;
  title: string;
  description?: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  /** Thème classique 1 avec questions désérialisées */
  menu_1?: MenuThemeDetail;
  /** Thème classique 2 avec questions désérialisées */
  menu_2?: MenuThemeDetail;
  /** Thème troll avec questions désérialisées */
  menu_troll?: MenuThemeDetail;
  burger_quiz_count: number;
}

/** POST /api/quiz/menus/ et PUT /api/quiz/menus/{id}/ */
export interface MenusInput {
  title: string;
  description?: string;
  original?: boolean;
  menu_1_id: string;
  menu_2_id: string;
  menu_troll_id: string;
  tags?: string[];
}

/** PATCH /api/quiz/menus/{id}/ */
export type MenusPatchInput = Partial<MenusInput>;
```

### Addition

```typescript
import { QuestionDetail, UserRef } from "../quiz";

// ─────────────────────────────────────────────
// Manche Addition
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/additions/ */
export interface AdditionList {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  burger_quiz_count: number;
}

/**
 * Détail dans GET /api/quiz/additions/{id}/
 *
 * Les questions sont désérialisées avec leur contenu complet.
 */
export interface AdditionDetail {
  id: string;
  title: string;
  description?: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions_count: number;
  /** Questions complètes avec texte et réponses, ordonnées */
  questions: QuestionDetail[];
  burger_quiz_count: number;
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/additions/ et PUT /api/quiz/additions/{id}/ */
export interface AdditionInput {
  title: string;
  description?: string;
  original?: boolean;
  question_ids: string[];
  tags?: string[];
}

/** PATCH /api/quiz/additions/{id}/ */
export type AdditionPatchInput = Partial<AdditionInput>;
```

### Burger de la mort

```typescript
import { QuestionDetail, UserRef } from "../quiz";

// ─────────────────────────────────────────────
// Manche Burger de la Mort
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/deadly-burgers/ */
export interface DeadlyBurgerList {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  burger_quiz_count: number;
}

/**
 * Détail dans GET /api/quiz/deadly-burgers/{id}/
 *
 * Les questions sont désérialisées avec leur contenu complet.
 */
export interface DeadlyBurgerDetail {
  id: string;
  title: string;
  original: boolean;
  author?: UserRef;
  tags: string[];
  created_at: string;
  updated_at: string;
  /** Exactement 10 questions de type DB, désérialisées */
  questions: QuestionDetail[];
  burger_quiz_count: number;
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/deadly-burgers/ et PUT /api/quiz/deadly-burgers/{id}/ */
export interface DeadlyBurgerInput {
  title: string;
  original?: boolean;
  /** Exactement 10 UUIDs de questions de type DB */
  question_ids: string[];
  tags?: string[];
}

/** PATCH /api/quiz/deadly-burgers/{id}/ */
export type DeadlyBurgerPatchInput = Partial<DeadlyBurgerInput>;
```

### Interludes vidéo

```typescript
import { InterludeType } from "./enums";
import { UserRef } from "./quiz";

// ─────────────────────────────────────────────
// VideoInterlude
// ─────────────────────────────────────────────

/** Item dans GET /api/quiz/interludes/ (liste) */
export interface VideoInterludeList {
  id: string;
  title: string;
  youtube_url: string;
  youtube_video_id: string;
  interlude_type: InterludeType;
  duration_seconds?: number;
  autoplay: boolean;
  skip_allowed: boolean;
  skip_after_seconds?: number;
  created_at: string;
  updated_at: string;
}

/** Détail dans GET /api/quiz/interludes/{id}/ */
export interface VideoInterludeDetail extends VideoInterludeList {
  author?: UserRef;
  tags: string[];
}

/** Référence minimale pour inclusion dans la structure */
export interface VideoInterludeRef {
  id: string;
  title: string;
  interlude_type: InterludeType;
  youtube_video_id: string;
}

// ── Inputs ────────────────────────────────────

/** POST /api/quiz/interludes/ */
export interface VideoInterludeInput {
  title: string;
  youtube_url: string;
  interlude_type?: InterludeType; // défaut IL
  duration_seconds?: number;
  autoplay?: boolean; // défaut true
  skip_allowed?: boolean; // défaut true
  skip_after_seconds?: number;
  tags?: string[];
}

/** PATCH /api/quiz/interludes/{id}/ */
export type VideoInterludePatchInput = Partial<VideoInterludeInput>;
```

### Structure du Burger Quiz

```typescript
import { ElementType, QuestionType, InterludeType } from "./enums";
import { VideoInterludeRef } from "./video-interlude";

// ─────────────────────────────────────────────
// BurgerQuizElement (structure ordonnée)
// ─────────────────────────────────────────────

/**
 * Élément dans la structure d'un Burger Quiz.
 * Peut être une manche (round) ou un interlude.
 */
export interface BurgerQuizElement {
  order: number;
  element_type: ElementType;
  /** Type de manche si element_type = "round" */
  round_type?: QuestionType;
  /** Interlude si element_type = "interlude" */
  interlude?: VideoInterludeRef;
}

/** Réponse GET /api/quiz/burger-quizzes/{id}/structure/ */
export interface BurgerQuizStructure {
  burger_quiz_id: string;
  elements: BurgerQuizElement[];
}

// ── Inputs ────────────────────────────────────

/** Élément pour PUT /api/quiz/burger-quizzes/{id}/structure/ */
export interface BurgerQuizElementInput {
  element_type: ElementType;
  /** Requis si element_type = "round" */
  round_type?: QuestionType;
  /** Requis si element_type = "interlude" */
  interlude_id?: string;
}

/** PUT /api/quiz/burger-quizzes/{id}/structure/ */
export interface BurgerQuizStructureInput {
  elements: BurgerQuizElementInput[];
}
```

## Session

```typescript
import { User } from "./auth";
import { BurgerQuizList } from "./burger-quiz";
import { SessionStatus, PlayerRole, Team } from "./enums";

// ─────────────────────────────────────────────
// Session de jeu 🚧
// ─────────────────────────────────────────────

export interface Player {
  id: string;
  user: User;
  team?: Team;
  role: PlayerRole;
  score: number;
  connected: boolean;
}

export interface GameSessionDetail {
  id: string;
  code: string;
  burger_quiz: BurgerQuizList;
  host: User;
  status: SessionStatus;
  players: Player[];
  current_round?: string;
  current_question_index?: number;
  scores: {
    ketchup: number;
    mayo: number;
  };
  created_at: string;
}

// ── Inputs ────────────────────────────────────

export interface CreateSessionInput {
  burger_quiz_id: string;
}

export interface JoinSessionInput {
  code: string;
  team?: Team;
}
```

## Organisation des fichiers

```
src/types/
├── index.ts            # Re-exports
├── enums.ts
├── auth.ts
├── api.ts
├── quiz.ts             # Question, Answer, UserRef
├── burger-quiz.ts
├── video-interlude.ts  # VideoInterlude
├── burger-quiz-element.ts # Structure ordonnée
├── session.ts
└── rounds/
    ├── index.ts
    ├── nuggets.ts
    ├── salt-or-pepper.ts
    ├── menus.ts
    ├── addition.ts
    └── deadly-burger.ts
```

---

## Notes sur la sérialisation

### Entrée vs Sortie

L'API utilise des formats différents en **entrée** (création/modification) et en **sortie** (lecture) :

| Champ                   | Entrée (POST/PUT/PATCH)                           | Sortie (GET)                                       |
| ----------------------- | ------------------------------------------------- | -------------------------------------------------- |
| Questions d'une manche  | `question_ids: string[]` (UUIDs)                  | `questions: QuestionDetail[]` (objets complets)    |
| Manches d'un BurgerQuiz | `nuggets_id`, `addition_id`, etc. (UUIDs)         | `nuggets`, `addition`, etc. (objets complets)      |
| Thèmes d'un Menus       | `menu_1_id`, `menu_2_id`, `menu_troll_id` (UUIDs) | `menu_1`, `menu_2`, `menu_troll` (objets complets) |

### Questions désérialisées

En lecture, les questions sont toujours retournées avec leur contenu complet :

- `id`, `text`, `question_type`
- `answers[]` avec `id`, `text`, `is_correct`
- `author`, `tags`, `created_at`, `updated_at`
- `explanations`, `video_url`, `image_url` (optionnels)

Cela permet d'afficher un Burger Quiz complet en une seule requête GET.
