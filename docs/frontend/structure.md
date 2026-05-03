# Structure du Frontend

> Arborescence du dossier `frontend/src/` :

```
frontend/src/
├── components/                   # Composants réutilisables
│   ├── common/                    # Composants partagés (non primitifs)
│   │   ├── PageLoader.tsx         # Fallback Suspense (lazy loading routes)
│   │   ├── separators.tsx         # OnionSeparator, LettuceSeparator
│   │   ├── StatsBadges.tsx        # Badges (Discord, Quiz Live, etc.)
│   │   ├── artwork/               # BurgerArtwork, ArtworkSubtitle
│   │   └── index.ts
│   │
│   ├── ui/                        # Primitives UI (shadcn/radix uniquement)
│   │   ├── alert.tsx
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   ├── use-toast.ts           # Hook toast (interface shadcn)
│   │   └── ...
│   │
│   ├── forms/                     # Formulaires (react-hook-form + zod)
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── index.ts
│   │
│   ├── layout/                    # Mise en page
│   │   ├── AuthLayout.tsx         # Layout pages publiques (login, register)
│   │   ├── PageWrapper.tsx        # Container responsive
│   │   ├── Layout.tsx             # Layout principal (pages protégées)
│   │   ├── Header.tsx, Nav.tsx, Footer.tsx
│   │   ├── header/                # Logo, MobileMenuToggle, MobileMenuPanel...
│   │   └── index.ts
│   │
│   └── PagePlaceholder.tsx        # Placeholder pages en construction
│
├── features/                      # Modules métier (feature-based)
│   ├── auth/
│   │   ├── api/                   # AUTH_ENDPOINTS (endpoints.ts)
│   │   ├── schemas/               # login.ts, register.ts (Zod)
│   │   └── index (ré-exports)
│   │
│   └── quiz/
│       ├── api/                   # quiz, nuggets, salt-pepper, menus, addition, deadly-burger, interludes, menu-themes, query-keys
│       └── (hooks dans features/rounds/nuggets/hooks.ts si présent)
│
├── lib/                           # Utilitaires et configuration
│   ├── axios.ts                   # apiClient + tokenStorage + intercepteurs JWT
│   ├── publicUrls.ts              # Endpoints publics (isPublicUrl)
│   ├── queryClient.ts             # QueryClient + config TanStack Query
│   ├── api-error.ts               # getApiErrorMessage
│   └── utils.ts                   # cn(), helpers
│
├── routes/                        # Config React Router
│   ├── index.ts                   # publicRoutes, protectedRoutes, ProtectedRoute, PublicRoute
│   ├── public.tsx                 # Routes publiques (auth, 404)
│   ├── utils.tsx                  # createCrudRoutes
│   ├── ProtectedRoute.tsx         # Guard auth (redirige vers login si non connecté)
│   ├── PublicRoute.tsx            # Redirige vers dashboard si déjà connecté
│   └── protected/                 # Routes protégées (dashboard, profile, play, quiz, drafts)
│       ├── index.ts
│       ├── dashboard.tsx, profile.tsx, drafts.tsx
│       ├── play/
│       └── quiz/                  # burger-quiz, addition, deadly-burger, menus, nuggets, salt-pepper, interludes
│
├── stores/                        # Stores Zustand globaux
│   ├── auth.ts                    # useAuthStore (user, isAuthenticated, isHydrated)
│   └── index.ts
│
├── types/                         # Types TypeScript globaux
│   ├── api.ts                     # PaginatedResponse...
│   ├── auth.ts                    # User, AuthTokens...
│   └── index.ts
│
├── pages/                         # Pages / routes
│   ├── auth/, profile/, play/, quiz/, rounds/, interludes/, drafts/
│   ├── HomePage.tsx, NotFoundPage.tsx
│   └── index.ts
│
├── providers/                     # Providers React globaux
│   ├── QueryProvider.tsx          # TanStack Query + Devtools
│   ├── theme (ThemeProvider)
│   └── index
│
├── theme/                         # Thème visuel (couleurs, fonts, appTheme, BackgroundEffects)
│
├── App.tsx                        # createBrowserRouter + Suspense + Layout + ProtectedRoute
├── App.css, main.tsx, index.css
```

## Organisation par domaine

| Dossier             | Responsabilité                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------ |
| `components/common` | Composants partagés (PageLoader, séparateurs, StatsBadges, artwork) — pas des primitifs UI |
| `components/ui`     | Primitives UI (shadcn/radix) + use-toast uniquement                                        |
| `components/forms`  | Formulaires (react-hook-form + zod)                                                        |
| `components/layout` | Structure de page (Header, Footer, Layout, AuthLayout)                                     |
| `features/`         | Modules métier — auth (api, schemas), quiz (api, query-keys)                               |
| `lib/`              | axios, publicUrls, queryClient, api-error, utils                                           |
| `routes/`           | Routes, ProtectedRoute, PublicRoute, createCrudRoutes                                      |
| `stores/`           | État global Zustand (auth)                                                                 |
| `types/`            | Types partagés                                                                             |
| `theme/`            | Couleurs, animations, effets visuels                                                       |

## Layouts

- **AuthLayout** : Pages publiques (login, register, etc.) — fond animé, pas de header/footer.
- **Layout** : Pages protégées — Header, Nav, contenu, Footer, séparateurs lettuce/onion.
- **PageWrapper** : Conteneur responsive (max-width, padding).

## Guards

- **ProtectedRoute** : Enveloppe les routes protégées ; redirige vers `/auth/login` si non connecté. Fichier : `src/routes/ProtectedRoute.tsx`.
- **PublicRoute** : Redirige vers `/dashboard` si déjà connecté (login/register). Fichier : `src/routes/PublicRoute.tsx`.
