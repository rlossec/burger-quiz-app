## Frontend Burger Quiz – Vue d'ensemble

Ce dossier documente l'architecture et les conventions du frontend.

## 1. Fichiers de référence

- **Structure & architecture**
  - `structure.md` – Arborescence de `frontend/src` et responsabilités de chaque dossier.
  - `types.md` – Types TypeScript partagés (auth, quiz, sessions, etc.).

- **Thème & UI**
  - `THEME.md` – Système de design (couleurs OKLCH, typographie, `appTheme`, layouts, backgrounds).
  - `components.md` (optionnel) – Catalogue des composants UI réutilisables (shadcn/ui + composants maison).

- **État global & logique métier**
  - `stores.md` – Stores Zustand transverses (`useAuthStore`, `useThemeStore`) et stores métier (`useQuizStructureStore`, `useGameStore`).

- **Routing & pages**
  - `page_reference.md` – Tableau des pages/routes (URLs, statut, liens vers wireframes).
  - `routing.md` – Détails d'implémentation du routing (React Router, routes publiques/protégées, redirections).

- **Auth & API**
  - `auth.md` – Gestion de l'authentification côté frontend (store, tokens, routes protégées).
  - `api.md` – Intégration API (axios configuré, interceptors, React Query).

- **Suivi du chantier**
  - `progress.md` – Bilan d'implémentation, décisions d'architecture, éléments restant à faire.

## 2. Stack et principes

- **Stack principale**
  - React + TypeScript
  - React Router v6 (configuration via `RouteObject` dans `src/routes`)
  - Zustand pour l'état global
  - React Query (`@tanstack/react-query`) pour les données serveur
  - axios comme client HTTP
  - shadcn/ui + Tailwind + thème maison (OKLCH) pour l'UI

- **Principes d'architecture**
  - **Séparation claire** :
    - Stores transverses dans `src/stores/`.
    - Stores métier dans `src/features/*/store.ts` (quiz, play à venir).
  - **Une seule source de vérité** pour chaque concept :
    - Notifications : toasts `shadcn/ui`.
    - Thème : couleurs/typographie centralisées dans `src/theme/` + store de thème pour le choix user.
  - **Routing structuré** :
    - `src/routes/public.tsx` pour les routes publiques (auth).
    - `src/routes/protected/*` pour les routes protégées (Dashboard, Quiz, Play, Profil).
    - `ProtectedRoute` pour la garde d'auth.
