## 1. Préparation

- [x] Vision → [BACKLOG.md](BACKLOG.md)
- [x] User stories → [BACKLOG.md](BACKLOG.md)
- [x] Modèles données → [models/README](../database/models/README.md)
- [x] Wireframes MVP → [wireframes/README](../frontend/wireframes/README.md)
- [x] Architecture → ARCHITECTURE.md
- [x] Stack → README.md
- [ ] Wireframes Session
- [ ] Wireframes Real time

## 2. Développement

### Backend

- [x] Squelette projet → README.md
- [x] Base données
- [x] API REFERENCE
- [x] Tests Quiz
- [x] Endpoints Quiz

### Frontend

#### Phase 1 – Planification fonctionnelle

- [ ] Liste des pages avec routes associées
- [ ] Définition des modèles front (types)
- [ ] Liste des états globaux (stores)
- [ ] Définition des flux (auth, quiz, session)

#### Phase 2 – Setup technique

- [x] React + TypeScript (Vite)
- [ ] React Router
- [ ] Tailwind + shadcn/ui
- [ ] TanStack Query
- [ ] ESLint + Prettier

#### Phase 3 – Layout global

- [ ] `<Layout>`
- [ ] `<Header>` / `<Nav>`
- [ ] `<Footer>`
- [ ] Container responsive

#### Phase 4 – Thème et design system

- [ ] ThemeProvider (dark/light)
- [ ] Définition du thème (couleurs, typographie)

#### Phase 5 – Routing et pages vides

- [ ] Créer les pages placeholder
- [ ] Configurer les routes

#### Phase 6 – Auth

- [ ] Login page
- [ ] Register Page
- [ ] Dashboard Placeholder
- [ ] Auth store (Zustand)
- [ ] ProtectedRoute

#### Phase 7 – Feature BurgerQuiz

- [ ] Types
- [ ] Service API
- [ ] Hooks TanStack Query
- [ ] Card component
- [ ] Pages

#### Phase 8 – Feature Play

- [ ] Store Zustand (quiz en cours)
- [ ] Question Player
- [ ] Timer
- [ ] Score
- [ ] Résultats

#### Phase 9 – UX polish

- [ ] Notifications (toast)
- [ ] Skeleton loaders
- [ ] Error boundaries
- [ ] Animations

## 3. Structure Frontend

```
src/
├── app/
│   ├── router.tsx          # Configuration React Router
│   └── providers.tsx       # Providers (Query, Theme, etc.)
│
├── components/
│   ├── layout/             # Layout, Header, Footer, Nav
│   ├── ui/                 # Composants shadcn/ui
│   └── common/             # Composants réutilisables
│
├── features/
│   ├── auth/
│   │   ├── api/
│   │   ├── hooks/
│   │   ├── components/
│   │   ├── store.ts
│   │   └── types.ts
│   │
│   ├── burger-quiz/
│   │   ├── api/
│   │   ├── hooks/
│   │   ├── components/
│   │   ├── pages/
│   │   └── types.ts
│   │
│   └── play/
│       ├── components/
│       ├── hooks/
│       └── store.ts
│
├── hooks/                  # Hooks globaux
├── services/               # Client API (axios)
├── lib/                    # Utilitaires
├── types/                  # Types globaux
├── styles/                 # Styles globaux
└── main.tsx
```

## 4. Contextes globaux

| Contexte            | Usage                        | Alternative          |
| ------------------- | ---------------------------- | -------------------- |
| AuthContext         | Authentification utilisateur | Zustand recommandé   |
| ThemeContext        | Toggle dark/light            | shadcn ThemeProvider |
| NotificationContext | Toasts / alertes             | Zustand ou sonner    |

## 5. Versions cibles

- **V0.1** – Création / Modification de Burger Quiz
- **V1.0** – Session de jeu Burger Quiz
- **V2.0** – Real time
