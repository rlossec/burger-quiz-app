## Intégration API

Documentation de la manière dont le frontend communique avec l'API backend : client HTTP axios, gestion des erreurs, configuration React Query et conventions pour les hooks.

---

## 1. Vue d'ensemble

- **Objectifs**
  - Avoir une **seule instance** axios configurée (`apiClient`).
  - Gérer les tokens JWT (injection + refresh) de façon centralisée.
  - Standardiser la configuration React Query (cache, retry, erreurs).
  - Définir des **conventions d'écriture des hooks** de données.

- **Pièces principales**
  - `src/lib/axios.ts` – Client HTTP configuré + gestion des tokens.
  - `src/lib/publicUrls.ts` – Définition des endpoints publics (regex + méthode) et `isPublicUrl()`.
  - `src/lib/api-error.ts` – `getApiErrorMessage(error)` pour extraire un message lisible des erreurs Axios.
  - `src/lib/queryClient.ts` – Instance `QueryClient` et options par défaut.
  - **Auth** : `src/features/auth/api/endpoints.ts` – Constantes des endpoints auth (`AUTH_ENDPOINTS`).
  - **Quiz** : `src/features/quiz/api/` – Modules par ressource (quiz, nuggets, salt-pepper, menus, addition, deadly-burger, interludes, menu-themes) et `query-keys.ts` (table de vérité des clés React Query).

---

## 2. Client HTTP `apiClient` (axios)

- **Fichier** : `src/lib/axios.ts`

### 2.1 Configuration de base

- `baseURL` : `import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'`.
- Headers par défaut :
  - `Content-Type: 'application/json'`.
- `withCredentials: false` (Choix : tokens dans les headers vs ~~cookies~~).

### 2.2 Gestion des tokens (`tokenStorage`)

- Implémenté dans le même fichier :
  - `getAccess()`, `getRefresh()`
  - `setTokens(access, refresh)`
  - `setAccess(access)`
  - `clear()`
- Tokens stockés dans `localStorage` (`access_token`, `refresh_token`).

> La logique de tokens est **purement HTTP** : le store d'auth ne les voit pas, il ne manipule que le `user`.

### 2.3 URLs publiques

- `PUBLIC_URLS` liste les endpoints ne nécessitant pas de token : login, endpoints d'activation / reset.
- Cas particulier :
  - POST `/auth/users/` (inscription) est explicitement considéré comme public.

**Fonction `isPublicUrl(url)`** :

- Permet aux interceptors d'ignorer la gestion de token pour ces routes.

### 2.4 Interceptor `request`

- Avant chaque requête :
  - Si `!isPublicUrl(config.url, config.method)` :
    - Récupère l'`access_token` via `tokenStorage.getAccess()`.
    - Ajoute `Authorization: Bearer <token>` s'il existe.

### 2.5 Interceptor `response` (refresh 401)

- Gestion des erreurs 401 :
  - Rejet immédiat si `isPublicUrl(config.url, config.method)` ou si la requête a déjà été retentée (`_retry`).
  - Gestion d'un booléen `isRefreshing` et d'une file `failedQueue` pour :
    - Mettre en attente les requêtes pendant qu'un refresh est en cours.
    - Les rejouer une fois le nouveau token obtenu.
- Flux de refresh :
  1. Lire le `refresh_token` via `tokenStorage.getRefresh()`.
  2. Appeler `POST {API_URL}/auth/jwt/refresh/` avec `{ refresh }`.
  3. Si succès :
     - Mettre à jour l'`access_token`.
     - Rejouer la requête initiale.
  4. Si échec ou absence de refresh token :
     - `tokenStorage.clear()`
     - Vider la queue en erreur.
     - Redirection vers `/auth/login`.

---

## 3. React Query – `queryClient`

- **Fichier** : `src/lib/queryClient.ts`

### 3.1 Helper d'erreur `getApiErrorMessage`

- But : extraire un message lisible depuis une `AxiosError`.
- Gère les formats de réponses typiques Django REST :
  - `{ detail: "..." }`
  - `{ field: ["message"] }`
  - String brute.
- Utilisé dans les callbacks d'erreur du `QueryCache` et du `MutationCache`.

### 3.2 Configuration du `QueryClient`

- `queryCache` :
  - `onError`: log en console uniquement si la query a déjà des données (erreur en background).
- `mutationCache` :
  - `onError`: log en console toutes les erreurs de mutation.

### 3.3 `defaultOptions.queries`

- `staleTime: 5 minutes` – durée pendant laquelle les données sont considérées fraîches.
- `gcTime: 10 minutes` – durée de rétention en cache après démontage.
- `refetchOnWindowFocus: import.meta.env.PROD` – en dev, pas de refetch au focus.
- `retry` :
  - Fonction custom :
    - Pas de retry sur les erreurs 4xx (400–499).
    - Sinon, max 2 tentatives.

### 3.4 `defaultOptions.mutations`

- `retry: false` – pas de retry automatique sur les mutations.

---

## 4. Conventions pour les hooks API

### 4.1 Endpoints

- **Fichiers** :
  - `src/features/auth/api/endpoints.ts` pour l'auth (`AUTH_ENDPOINTS`).
  - `src/features/quiz/api/*` pour les domaines quiz.
- Les chemins sont centralisés **par feature** (et non dans un `src/api/endpoints.ts` global).

### 4.2 Modules API

- **Structure actuelle** : `src/features/<feature>/api/*.ts`.
  - Exemples : `src/features/quiz/api/quiz.ts`, `nuggets.ts`, `menus.ts`, `interludes.ts`, `tags.ts`.
  - Export central : `src/features/quiz/api/index.ts`.
- Les modules API exportent des fonctions/facades HTTP pures (sans React) qui sont ensuite utilisées par les hooks React Query.

> **Bon pattern** : séparer les fonctions "API pures" (qui parlent à axios) des hooks React Query (qui parlent à React).

### 4.3 Hooks React Query

- Nommage :
  - Queries : `useQuizListQuery`, `useQuizDetailQuery`, etc.
  - Mutations : `useCreateQuizMutation`, `useUpdateQuizMutation`, etc.
- Clés de query :
  - Table de vérité pour les clés (optionnel) :
    - `['quiz', 'list']`, `['quiz', id]`, `['nuggets', 'list']`, etc.
  - Utiliser des clés stables pour pouvoir invalider précisément (`queryClient.invalidateQueries`).

### 4.4 Exemple type (schématique)

```ts
// src/api/quiz.ts
import { apiClient } from "@/lib/axios";
import type { Quiz, QuizInput } from "@/types/quiz";

export const fetchQuizList = async (): Promise<Quiz[]> => {
  const { data } = await apiClient.get("/quiz/");
  return data;
};

export const createQuiz = async (payload: QuizInput): Promise<Quiz> => {
  const { data } = await apiClient.post("/quiz/", payload);
  return data;
};
```

```ts
// src/features/quiz/hooks.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchQuizList, createQuiz } from "@/api/quiz";

export const useQuizListQuery = () =>
  useQuery({ queryKey: ["quiz", "list"], queryFn: fetchQuizList });

export const useCreateQuizMutation = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createQuiz,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["quiz", "list"] });
    },
  });
};
```

---

## 5. Gestion des erreurs côté UI

### 5.1 Stratégie générale

- Les erreurs techniques (réseau, 500, etc.) sont loguées par défaut via `QueryCache`/`MutationCache`.
- Pour l'UX, on s'appuie sur les **toasts `shadcn/ui`** et/ou des messages intégrés dans les formulaires.

### 5.2 Intégration avec les toasts

- Recommandation :
  - Utiliser `getApiErrorMessage(error)` dans les hooks de mutation/query.
  - Afficher un toast d'erreur avec ce message.

Exemple :

```ts
import { useMutation } from "@tanstack/react-query";
import { getApiErrorMessage } from "@/lib/api-error";
import { useToast } from "@/components/ui/use-toast";

export const useCreateQuizMutation = () => {
  const { toast } = useToast();

  return useMutation({
    mutationFn: createQuiz,
    onError: (error) => {
      toast({
        variant: "destructive",
        title: "Erreur lors de la création du quiz",
        description: getApiErrorMessage(error),
      });
    },
  });
};
```

### 5.3 Liens avec l'auth

- En cas de `401` :
  - Le refresh est géré par `axios.ts`.
  - En cas d'échec de refresh, l'utilisateur est redirigé vers `/auth/login`.
  - On peut compléter en affichant un toast de type :
    - “Votre session a expiré, veuillez vous reconnecter.”

---

## 6. Hooks Quiz (`src/features/quiz/hooks/`)

### 6.1 Architecture

- **Modules API** (`api/*.ts`) : fonctions pures HTTP, sans React.
- **Hooks** (`hooks/*.ts`) : wrappers React Query + toasts shadcn.
- **Query keys** (`api/query-keys.ts`) : table de vérité des clés de cache.

### 6.2 Query keys

**Rôle** : identifier de façon stable chaque entrée du cache React Query.

- **Forme** : tableau de valeurs primitives, ex. `['quiz', 'list']`, `['quiz', id]`.
- **Centralisation** : toujours importer depuis `query-keys.ts`, jamais de clé inline.
- **Usage** :
  - Queries : `queryKey: queryKeys.quiz.lists()`
  - Invalidations : `queryClient.invalidateQueries({ queryKey: queryKeys.quiz.lists() })`

**Hiérarchie typique par ressource** :

- `all()` : préfixe global (ex. `['quiz']`) — invalide tout le domaine.
- `lists()` : listes paginées (ex. `['quiz', 'list']`).
- `detail(id)` : détail d'un élément (ex. `['quiz', id]`).
- Cas particulier : `structure(id)` pour la structure d'un Burger Quiz.

### 6.3 Mutations

**Rôle** : modifier les données côté serveur et garder le cache cohérent.

- **`mutationFn`** : appelle la fonction API pure (`quizApi.create`, etc.).
- **`onSuccess`** : invalide les queries concernées pour forcer un refetch :
  - Création → invalider `lists()`.
  - Mise à jour → invalider `detail(id)` et éventuellement `lists()`.
  - Suppression → invalider `lists()`.
- **`onError`** : toast destructif avec `getApiErrorMessage(error)` via `useToast()`.

### 6.4 Flux global

1. **API** (`api/*.ts`) : fonctions pures HTTP.
2. **Hooks query** : `useQuery` avec `queryKey` + `queryFn`.
3. **Hooks mutation** : `useMutation` avec invalidation + toasts.
4. **Composants** : consomment les hooks, appellent `mutate` / `mutateAsync`.

### 6.5 Fichiers hooks

| Fichier                     | Ressource     | Queries                 | Mutations                     |
| --------------------------- | ------------- | ----------------------- | ----------------------------- |
| `useBurgerQuizQueries.ts`   | Burger Quiz   | list, detail, structure | create, update, delete        |
| `useNuggetsQueries.ts`      | Nuggets       | list, detail            | create, update, patch, delete |
| `useSaltPepperQueries.ts`   | Salt & Pepper | list, detail            | create, update, patch, delete |
| `useMenusQueries.ts`        | Menus         | list, detail            | create, update, patch, delete |
| `useMenuThemesQueries.ts`   | Menu Themes   | list, detail, byType    | create, update, patch, delete |
| `useAdditionQueries.ts`     | Addition      | list, detail            | create, update, patch, delete |
| `useDeadlyBurgerQueries.ts` | Deadly Burger | list, detail            | create, update, patch, delete |
| `useInterludesQueries.ts`   | Interludes    | list, detail            | create, update, patch, delete |

---

## 7. Bonnes pratiques

- Toujours utiliser `apiClient` (pas `axios` brut) pour bénéficier des interceptors.
- Ne pas réimplémenter de logique de tokens dans les features :
  - Utiliser `tokenStorage` + `useAuthStore` là où nécessaire.
- Pour chaque nouveau domaine métier :
  - Créer des fichiers API dans `src/features/<domaine>/api/`.
  - Créer des hooks React Query dans `src/features/<domaine>/hooks/`.
- Grouper les messages d'erreur dans une même logique (toasts + `getApiErrorMessage`) pour garder une UX cohérente sur tout le frontend.

---

## Voir aussi

- [Routing et lazy loading](./routing.md) – Structure des routes protégées, lazy loading des pages, modèle burger-quiz et `createCrudRoutes`.
