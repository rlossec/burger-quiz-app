# Routing et lazy loading

Documentation de la structure des routes protégées et du chargement paresseux des pages (code splitting).

---

## 1. Vue d'ensemble

- **Objectifs**
  - Réduire le bundle initial en chargeant chaque page (ou groupe de pages) à la demande.
  - Garder des **exports nommés** pour les pages (pas d'`export default`).
  - Un **seul `Suspense`** à la racine pour toutes les routes lazy.

- **Pièces principales**
  - `src/App.tsx` – `<Suspense fallback={<PageLoader />}>` autour de `RouterProvider`.
  - `src/components/common/PageLoader.tsx` – Fallback affiché pendant le chargement d'une route.
  - `src/routes/utils.tsx` – `createCrudRoutes()` pour les routes CRUD (list, create, detail, edit).
  - `src/routes/protected/quiz/*.tsx` – Définition des routes par domaine avec `lazy()`.

---

## 2. Stratégie de lazy loading

### 2.1 Pourquoi `lazy()` avec exports nommés ?

- `React.lazy()` attend un module avec un **export default**.
- On préfère garder des **exports nommés** dans les pages pour la cohérence et le refactoring.
- On adapte le chargement dynamique en renvoyant un objet `{ default: Composant }` :

```ts
const BurgerQuizListPage = lazy(() =>
  import("@/pages/quiz/BurgerQuizListPage").then((m) => ({
    default: m.BurgerQuizListPage,
  })),
);
```

- Chaque page reste exportée en nommé : `export function BurgerQuizListPage() { ... }`.

### 2.2 Un seul Suspense en racine

- Un `<Suspense>` est placé **une seule fois** dans l'arbre, autour de `RouterProvider` dans `App.tsx`.
- Dès qu'une route rend un composant lazy, React suspend et remonte jusqu'à ce Suspense, qui affiche `PageLoader`.
- **À éviter** : un Suspense par route ou par layout, qui alourdit la config sans bénéfice.

Exemple dans `App.tsx` :

```tsx
<Suspense fallback={<PageLoader />}>
  <RouterProvider router={router} />
</Suspense>
```

---

## 3. Modèle de fichier de routes : Burger Quiz

Référence : `src/routes/protected/quiz/burger-quiz.tsx`.

- Import de `lazy` depuis React et de `RouteObject` depuis react-router-dom.
- Pour chaque page : `lazy(() => import('@/pages/...').then((m) => ({ default: m.NomDuComposant })))`.
- Export d'un tableau `RouteObject[]` avec `path` et `element: <Composant />`.

```tsx
import { lazy } from "react";
import type { RouteObject } from "react-router-dom";

const BurgerQuizListPage = lazy(() =>
  import("@/pages/quiz/BurgerQuizListPage").then((m) => ({
    default: m.BurgerQuizListPage,
  })),
);
const BurgerQuizCreatePage = lazy(() =>
  import("@/pages/quiz/BurgerQuizCreatePage").then((m) => ({
    default: m.BurgerQuizCreatePage,
  })),
);
const BurgerQuizDetailEdit = lazy(() =>
  import("@/pages/quiz/BurgerQuizDetailEdit").then((m) => ({
    default: m.BurgerQuizDetailEdit,
  })),
);

export const burgerQuizRoutes: RouteObject[] = [
  { path: "quiz", element: <BurgerQuizListPage /> },
  { path: "quiz/create", element: <BurgerQuizCreatePage /> },
  { path: "quiz/:id", element: <BurgerQuizDetailEdit /> },
];
```

---

## 4. Routes CRUD : `createCrudRoutes`

Pour les manches (addition, deadly-burger, menus, nuggets, salt-pepper) et les interludes, les routes suivent le même schéma CRUD :

- `basePath` → liste
- `basePath/create` → création
- `basePath/:id` → détail
- `basePath/:id/edit` → édition

Le helper `createCrudRoutes(basePath, { List, Create, Detail, Edit })` dans `src/routes/utils.tsx` génère ces quatre routes. Les composants passés peuvent être des **composants lazy** : ils sont des `ComponentType`, donc compatibles.

### 4.1 Modèle pour un domaine CRUD

Même pattern que burger-quiz : lazy + `.then((m) => ({ default: m.NomComposant }))`, puis passage des composants à `createCrudRoutes`.

Exemple : `src/routes/protected/quiz/nuggets.tsx`

```tsx
import { lazy } from "react";
import { createCrudRoutes } from "../../utils";

const NuggetsListPage = lazy(() =>
  import("@/pages/rounds/nuggets/NuggetsListPage").then((m) => ({
    default: m.NuggetsListPage,
  })),
);
const NuggetsCreatePage = lazy(() =>
  import("@/pages/rounds/nuggets/NuggetsCreatePage").then((m) => ({
    default: m.NuggetsCreatePage,
  })),
);
const NuggetsDetailPage = lazy(() =>
  import("@/pages/rounds/nuggets/NuggetsDetailPage").then((m) => ({
    default: m.NuggetsDetailPage,
  })),
);
const NuggetsEditPage = lazy(() =>
  import("@/pages/rounds/nuggets/NuggetsEditPage").then((m) => ({
    default: m.NuggetsEditPage,
  })),
);

export const nuggetsRoutes = createCrudRoutes("/nuggets", {
  List: NuggetsListPage,
  Create: NuggetsCreatePage,
  Detail: NuggetsDetailPage,
  Edit: NuggetsEditPage,
});
```

### 4.2 Fichiers concernés

| Fichier             | basePath         | Pages (dossier)                  |
| ------------------- | ---------------- | -------------------------------- |
| `addition.tsx`      | `/addition`      | `@/pages/rounds/addition/*`      |
| `deadly-burger.tsx` | `/deadly-burger` | `@/pages/rounds/deadly-burger/*` |
| `menus.tsx`         | `/menus`         | `@/pages/rounds/menus/*`         |
| `nuggets.tsx`       | `/nuggets`       | `@/pages/rounds/nuggets/*`       |
| `salt-pepper.tsx`   | `/salt-pepper`   | `@/pages/rounds/salt-pepper/*`   |
| `interludes.tsx`    | `/interludes`    | `@/pages/interludes/*`           |

---

## 5. Règles à suivre

- **Nouvelle route protégée** : définir les composants en `lazy()` avec le pattern `.then((m) => ({ default: m.NomExport }))`, et les passer soit en tableau `RouteObject[]` soit à `createCrudRoutes`.
- **Nouvelles pages** : exporter en **nommé** (`export function MaPage()`) pour rester cohérent avec le lazy loading.
- Ne pas ajouter de `Suspense` par route : le Suspense racine dans `App.tsx` suffit.
- Les chemins d'import des pages doivent pointer vers le fichier du composant (ex. `@/pages/rounds/nuggets/NuggetsListPage`), pas vers un barrel `@/pages` qui empêcherait le code splitting ciblé.

---

## Voir aussi

- [Intégration API (axios + React Query)](./api.md) – Client HTTP, tokens, React Query, query keys et hooks.
