## Bilan d'avancement frontend

Ce document synthétise l'état d'avancement du frontend.

---

## 1. Vue d'ensemble

- **Préparation** : 100% (vision, user stories, modèles, wireframes MVP, architecture, stack).
- **Backend socle** : 100% (base de données, API Quiz + tests, endpoints principaux).
- **Frontend – Setup & layout** : ~100% (stack, routing, layout global) – phases 2–5 du ROADMAP.
- **Frontend – Auth & stores de base** : ~80% (auth technique OK, `AuthStore` en place, autres stores spécifiés mais peu câblés dans l'UI).
- **Feature BurgerQuiz (édition)** : ~30% (types + backend prêts, stores de structure posés, UI encore à dérouler).
- **Feature Play (session de jeu)** : ~10% (`GameStore` amorcé dans la doc, peu d'écrans finalisés).
- **UX polish (toasts, loaders, erreurs, animations)** : ~10% (design posé pour les notifications, intégration partielle).

---

## 2. Détail par domaine

## 1. Thème (design system)

- **Architecture actuelle**
  - Layouts (`AuthLayout`, `Layout`, `Header`, `Footer`)
  - Fichiers en place dans `frontend/src/theme` :
    - `colors.ts` : palette
    - `fonts.ts`: la typo
    - `tailwind.ts` : les classes Tailwind pré-composées (`appTheme`).
  - Variables CSS racine (couleurs OKLCH : `--ketchup`, `--mustard`, `--denim`, etc.) définies dans `App.css`.

- **État d'avancement**
  - **✅ Palette de couleurs** : définie et documentée dans `THEME.md`.
  - **✅ Typographie** : `appTheme.typography` défini (h1–xs) + conventions d'usage.
  - **✅ Boutons & états** : `appTheme.buttons` (primary, secondary, outline, ghost, team) et intégration prévue avec les composants `Button` (`shadcn/ui`).
  - **✅ Layout & navigation** : `appTheme.layout`, `appTheme.nav`, `appTheme.logo`, `appTheme.footer` définis et consommés par les composants de layout.
  - **✅ Effets de fond** : `ThemeBackground` opérationnel (blobs, particules, grain).
  - **🚧 Page de test / design system** : routes `/drafts`, `/drafts/colors`, `/drafts/typography`, `/drafts/buttons`, `/drafts/cards`, `/drafts/forms` existent et pointent vers les pages de démonstration. Temporaires

- **Améliorations possibles**
  - Centraliser systématiquement les classes Tailwind via `appTheme` pour les nouvelles pages (éviter les classes “brutes” dispersées).

---

## 2. Stores (états globaux)

### 2.1 AuthStore

- **Implémentation**
  - Store défini dans `frontend/src/stores/authStore.ts`
  - Utilise **Zustand** + `persist` + `createJSONStorage` pour stocker :
    - `user: User | null`
    - `isAuthenticated: boolean`
    - `isHydrated: boolean`
  - Persistance dans `localStorage` sous la clé `auth-storage` (user + isAuthenticated).
  - Selectors dédiés : `selectUser`, `selectIsAuthenticated`, `selectIsHydrated`.

- **Intégration**
  - `ProtectedRoute` consomme `useAuthStore` :
    - Spinner de chargement tant que `isHydrated === false`.
    - Redirection vers `/login` si `!isAuthenticated`, en conservant la location dans `state.from`.
  - Les **tokens JWT** ne sont pas dans le store : ils sont gérés séparément via `tokenStorage` (`frontend/src/lib/axios.ts`).

- **État**
  - **✅ Logique de base** (login/logout/setUser/updateUser + hydratation) en place.
  - **✅ Persistance user / isAuthenticated** fonctionnelle.
  - **✅ Intégration minimaliste dans la protection des routes** via `ProtectedRoute`.
  - **🚧 Utilisation dans les pages d'auth** (login/register/profile) : à conforter/standardiser (hooks, helpers, gestion des messages d'erreur).

### 2.2 ThemeStore

- **Implémentation prévue**
  - Spécifiée dans `docs/frontend/stores.md` comme `src/stores/theme.ts` avec :
    - `theme: "light" | "dark" | "system"`
    - `setTheme`, `toggleTheme` + persistance localStorage (`theme-storage`).
  - Exemple d'intégration via un composant `ThemeProvider` qui applique la classe `light`/`dark` sur `document.documentElement`.

- **État**
  - **✅ Design documenté** dans `stores.md` (contrat clair).
  - **🚧 À vérifier / brancher** :
    - Présence effective de `src/stores/theme.ts` dans le code courant.
    - Ajout du `ThemeProvider` autour de l'app (ou dans le layout racine) pour relier le store au DOM.
    - UI pour changer le thème (toggle dans le header / menu utilisateur).

### 2.3 Notifications (shadcn / toasts)

- **Implémentation actuelle**
  - Utilisation du système de toasts shadcn via `components/ui/use-toast.ts` :
    - Hook `useToast()` pour déclencher des toasts.
    - Composant global `Toaster` monté dans l'arbre (via layout/providers) pour l'affichage.
  - Les mutations React Query (create/edit/delete) peuvent appeler `toast({ title, description, variant })`
    directement au niveau des hooks / composants.

- **Principe de fonctionnement**
  - Les notifications sont **éphémères** et gérées par shadcn (pas stockées dans un store global).
  - Possibilité de centraliser quelques helpers (ex. `showSuccessToast`, `showErrorToast`) dans un module
    utilitaire (ex. `lib/notifications.ts`) qui wrappe `useToast`.

- **État**
  - **✅ Système de toasts technique** disponible via shadcn.
  - **🚧 Standardisation** :
    - À harmoniser : usage cohérent des toasts dans les mutations React Query (succès/erreurs).
    - À documenter : conventions de wording (titres, descriptions) pour les principales actions (création, édition, suppression).

### 2.4 QuizStructureStore

- **QuizStructureStore**
  - Stocke la structure ordonnée d'un Burger Quiz en édition (`quizId`, `elements`, `isDirty`, `isSaving`).
  - Actions pour réordonner, ajouter/supprimer des interludes, marquer dirty/clean, reset.
  - **Usage principal** : éditeur de structure (`QuizStructureEditor`, `StructureElement`, etc.).

### 2.5. GameStore

- **GameStore**
  - Gère l'état de la session de jeu (`session`, `currentPlayer`, `phase`, `currentQuestion`, `scores`, timer, etc.).
  - Actions pour avancer les questions, gérer le timer, mettre à jour les scores et players.
  - **Statut** : marqué 🚧 dans la doc, logique de base déjà posée, mais intégration complète avec les pages `/play/*` encore en cours.

---

## 3. Authentification frontend

### 3.1 Gestion des tokens & API

- **Client HTTP (`frontend/src/lib/axios.ts`)**
  - `apiClient` configuré avec `baseURL = VITE_API_URL` et `Content-Type: application/json`.
  - **Injection automatique du token** :
    - Interceptor `request` qui ajoute `Authorization: Bearer <access>` sauf pour les URLs publiques (`/auth/jwt/create/`, `/auth/jwt/refresh/`, endpoints d'activation/reset, inscription).
  - **Refresh automatique** :
    - Interceptor `response` qui intercepte les `401` non publics.
    - Mécanisme de file d'attente (`failedQueue`) pour sérialiser les requêtes pendant le refresh.
    - Appel à `POST /auth/jwt/refresh/` avec le refresh token.
    - Mise à jour du token d'accès + re-jeu de la requête initiale.
    - En cas d'échec ou de refreshToken manquant : purge des tokens + redirection vers `/login`.

- **Stockage des tokens (`tokenStorage`)**
  - `getAccess`, `getRefresh`, `setTokens`, `setAccess`, `clear`.
  - Stockage direct dans `localStorage` sous les clés `access_token` et `refresh_token`.

- **État**
  - **✅ Gestion technique des tokens** (stockage, injection, refresh, redirection login) en place.
  - **✅ Séparation claire store auth / tokens** (le store ne connaît que le `user`).
  - **🚧 Gestion des erreurs côté UI** (messages pour expirations de session, etc.) à harmoniser avec le système de notifications.

### 3.2 React Query (`frontend/src/lib/queryClient.ts`)

- `QueryClient` configuré avec :
  - `staleTime` 5 minutes, `gcTime` 10 minutes.
  - `refetchOnWindowFocus` activé uniquement en production.
  - Politique de `retry` qui évite les retries sur erreurs 4xx.
  - Logs d'erreur centralisés pour queries et mutations (`getApiErrorMessage` pour extraire un message lisible).

- **Lien avec l'auth**
  - Les erreurs d'auth (401) sont déjà gérées par l'interceptor axios → React Query reçoit soit la réponse OK (après refresh), soit l'erreur finale après redirection/login.
  - **À faire** : brancher systématiquement les erreurs de mutation/query sur les **toasts shadcn** (`useToast`) pour une UX cohérente.

### 3.3 Routes publiques / protégées

- **Routing v2 (basé sur `RouteObject`)**
  - Routes protégées agrégées dans `frontend/src/routes/protected/index.ts` via :
    - `dashboardRoutes`, `profileRoutes`, `playRoutes`, `quizRoutes`.
  - `ProtectedRoute` utilisé comme wrapper pour les segments nécessitant l'auth (cf. doc `page_reference.md`).

- **Conduite utilisateur**
  - Si l'utilisateur n'est pas authentifié :
    - Interdiction d'accès aux routes protégées (redirigé vers `/login`).
    - La location actuelle est passée dans `state.from` pour un éventuel redirect post-login.
  - Si utilisateur déjà connecté et tente `/login`/`/register` :
    - Comportement souhaité (doc) : rediriger vers `/dashboard` (à vérifier dans les pages d'auth).

- **État**
  - **✅ Protection de base via `ProtectedRoute`** opérationnelle.
  - **✅ Découpage public/protégé** clair dans la doc (`page_reference.md`).
  - **🚧 Harmonisation** :
    - Vérifier que toutes les nouvelles routes protégées (version route objects) passent bien par `ProtectedRoute`.
    - Aligner les redirections après login/register avec les conventions de la doc (`redirect` param → `/dashboard`).

---

## 4. Synthèse rapide

- **Thème** : fondations solides (palette, typographie, layout, effets de fond, pages `/drafts/*` existantes). Reste surtout à enrichir la page de design system et à s'assurer de l'usage systématique d'`appTheme`.
- **Stores** : architecture Zustand claire et documentée (`AuthStore`, `ThemeStore`, `QuizStructureStore`, `GameStore`). Le code d'`AuthStore` est en place et utilisé, les autres stores sont définis ou spécifiés et à vérifier/câbler côté UI.
- **Notifications** : utilisation du système de toasts shadcn (`useToast` + `Toaster`) ; reste à standardiser l'usage dans les mutations React Query.
- **Auth frontend** : pipeline technique complet (tokens + refresh + interception + redirection) déjà en place via `axios.ts` + `useAuthStore` + `ProtectedRoute`. Le travail restant est surtout d'UX : messages toasts, cohérence des redirections, intégration fine dans toutes les pages d'auth et de profil.
