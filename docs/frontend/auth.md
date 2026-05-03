## Authentification frontend

Documentation de la gestion de l'authentification côté frontend : store, tokens JWT, routes publiques/protégées et flux principaux.

---

## 1. Vue d'ensemble

- **Objectifs**
  - Savoir si un utilisateur est connecté (`useAuthStore`).
  - Stocker les tokens JWT en sécurité raisonnable côté frontend.
  - Protéger les routes sensibles et gérer les redirections (login, logout, expiration).
  - Limiter le couplage : le store gère les **données utilisateur**, l'API gère les **tokens**.

- **Pièces principales**
  - `src/stores/authStore.ts` – Store Zustand d'authentification.
  - `src/lib/axios.ts` – Client HTTP + gestion des tokens (stockage, injection, refresh).
  - `src/routes/public.tsx` – Routes publiques (login, register, reset, etc.).
  - `src/routes/protected/*` – Routes protégées (Dashboard, Quiz, Play, Profil).
  - `src/routes/ProtectedRoute.tsx` – Garde d'authentification pour les routes protégées.

---

## 2. Store d'authentification (`useAuthStore`)

- **Fichier** : `src/stores/authStore.ts`
- **State** :
  - `user: User | null` – utilisateur connecté.
  - `isAuthenticated: boolean` – dérivé de `user` ou explicite.
  - `isHydrated: boolean` – indique que la réhydratation depuis `localStorage` est terminée.
- **Actions** :
  - `setUser(user | null)`
  - `login(user)`
  - `logout()`
  - `updateUser(data: Partial<User>)`
  - `setHydrated(boolean)`
- **Persistance** :
  - Stockage dans `localStorage` via `zustand/middleware/persist` sous la clé `auth-storage`.
  - On ne persiste que `user` et `isAuthenticated` (les tokens sont gérés ailleurs).

**Sélecteurs exportés** :

- `selectUser`
- `selectIsAuthenticated`
- `selectIsHydrated`

> **Règle** : dans les composants, utiliser les sélecteurs (`useAuthStore(selectIsAuthenticated)`) plutôt que de lire tout le store pour limiter les re-renders.

---

## 3. Tokens JWT et client HTTP

- **Fichier** : `src/lib/axios.ts`

### 3.1 Stockage des tokens (`tokenStorage`)

- **Stockage dans `localStorage`** :
  - `access_token`
  - `refresh_token`
- **API** :
  - `getAccess()`, `getRefresh()`
  - `setTokens(access, refresh)`
  - `setAccess(access)`
  - `clear()` – supprime les deux tokens.

> Le store d'auth **ne connaît pas** les tokens : il ne stocke que l'utilisateur.  
> Cela permet de garder `useAuthStore` indépendant de la couche HTTP.

### 3.2 Instance `apiClient`

- `apiClient` est une instance axios avec :
  - `baseURL = VITE_API_URL` (`http://localhost:8000/api` par défaut).
  - `Content-Type: application/json`.

#### Interceptor `request`

- Injecte automatiquement `Authorization: Bearer <access>`:
  - Sauf pour les URLs publiques (`/auth/jwt/create/`, `/auth/jwt/refresh/`, endpoints d'activation/reset, `/auth/users/` pour l'inscription).

#### Interceptor `response` (refresh automatique)

- Pour chaque réponse :
  - Si c'est un `401` sur une **route protégée** et que la requête n'a pas déjà été retentée :
    - Tente un refresh via `POST /auth/jwt/refresh/` avec le `refresh_token`.
    - Met à jour le `access_token` et rejoue la requête initiale.
  - Gestion d'une **file d'attente** (`failedQueue`) pour les requêtes qui arrivent pendant qu'un refresh est en cours.
  - En cas d'échec ou d'absence de refresh token :
    - `tokenStorage.clear()`
    - Redirection vers `/auth/login` via `window.location.href = '/auth/login'`.

> Résultat : la plupart des composants ne s'occupent pas de la gestion fine des 401 ; le flux normal est géré dans `axios.ts`.

---

## 4. Routes publiques et protégées

### 4.1 Routes publiques

- **Fichier** : `src/routes/public.tsx`
- Routes définies comme tableau :
  - `/auth/login`, `/auth/register` (sous layout `/auth`)
  - Alias : `/login` → `/auth/login`, `/register` → `/auth/register`
  - `/auth/activate/:uid/:token`
  - `/auth/resend-activation`
  - `/auth/forgot-password`
  - `/auth/password/reset/confirm/:uid/:token`
  - `/auth/email-sent`

Ces routes ne nécessitent pas d'être connecté.  
Les endpoints backend correspondants sont marqués comme “publics” dans `axios.ts` (pas de token requis).

### 4.2 Routes protégées

- **Fichier** : `src/routes/protected/index.ts`
- Agrège les routes métiers :
  - `dashboardRoutes`, `profileRoutes`, `playRoutes`, `quizRoutes`.
- Ces routes sont rendues **à l'intérieur** d'un wrapper `ProtectedRoute` pour garantir l'auth.

---

## 5. `ProtectedRoute` – garde d'authentification

- **Fichier** : `src/routes/ProtectedRoute.tsx`

Rôle :

- Attendre que `useAuthStore` soit réhydraté (`isHydrated`).
- Vérifier `isAuthenticated`.
- En fonction de l'état, rendre :
  - Un **spinner de chargement** tant que `!isHydrated`.
  - Une **redirection vers `/auth/login`** si non authentifié, avec `state.from = location` et `?redirect=...`.
  - Le contenu enfant (`<Outlet />`) sinon.

> **Pattern recommandé** : toutes les routes protégées doivent être sous ce wrapper.  
> Ainsi, on ne duplique pas les vérifications d'authentification dans chaque page.
