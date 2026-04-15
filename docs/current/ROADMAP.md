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
- [x] API REFERENCE Quiz
- [x] Tests Quiz
- [x] Endpoints Quiz

### Frontend

#### Phase 1 – Planification fonctionnelle

- [x] Liste des pages avec routes associées → [page_reference.md](../frontend/page_reference.md) (dans `docs/frontend/`)
- [x] Définition des modèles front (types) → [types.md](../frontend/types.md)
- [x] Liste des états globaux (stores) → [stores.md](../frontend/stores.md) (dans `docs/frontend/`)
- [x] Définition des flux (auth, quiz, session) → [flows/](../frontend/flows/README.md) (dans `docs/`)

#### Phase 2 – Setup technique

- [x] React + TypeScript (Vite)
- [x] React Router
- [x] Tailwind + shadcn/ui
- [x] TanStack Query
- [x] ESLint + Prettier

#### Phase 3 – Layout global

- [x] `<Layout>`
- [x] `<Header>` / `<Nav>`
- [x] `<Footer>`
- [x] Container responsive

#### Phase 4 – Thème et design system

- [x] ThemeProvider (dark/light)
- [x] Définition du thème (couleurs, typographie)

#### Phase 5 – Routing et pages vides

- [x] Créer les pages placeholder
- [x] Configurer les routes

#### Phase 6 – Auth

- [x] Login page
- [x] Register Page
- [x] Auth store (Zustand)
- [x] ProtectedRoute

#### Phase 7 – Feature BurgerQuiz

- [x] Types
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

## 5. Versions cibles

- **V0.1** – Création / Modification de Burger Quiz
- **V1.0** – Session de jeu Burger Quiz
- **V2.0** – Real time
