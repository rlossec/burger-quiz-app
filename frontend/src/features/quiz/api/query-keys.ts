/**
 * Clés TanStack Query pour le domaine Quiz (burger-quiz + manches).
 * Toujours importer depuis ce fichier — ne jamais écrire de clé inline.
 */
export const queryKeys = {
  quiz: {
    all: () => ['quiz'] as const,
    lists: () => ['quiz', 'list'] as const,
    detail: (id: string) => ['quiz', id] as const,
    structure: (id: string) => ['quiz', id, 'structure'] as const,
  },

  nuggets: {
    all: () => ['nuggets'] as const,
    lists: () => ['nuggets', 'list'] as const,
    detail: (id: string) => ['nuggets', id] as const,
  },

  saltPepper: {
    all: () => ['salt-pepper'] as const,
    lists: () => ['salt-pepper', 'list'] as const,
    detail: (id: string) => ['salt-pepper', id] as const,
  },

  menus: {
    all: () => ['menus'] as const,
    lists: () => ['menus', 'list'] as const,
    detail: (id: string) => ['menus', id] as const,
  },

  menuThemes: {
    all: () => ['menu-themes'] as const,
    lists: () => ['menu-themes', 'list'] as const,
    detail: (id: string) => ['menu-themes', id] as const,
    byType: (type: 'CL' | 'TR') => ['menu-themes', 'list', type] as const,
  },

  addition: {
    all: () => ['addition'] as const,
    lists: () => ['addition', 'list'] as const,
    detail: (id: string) => ['addition', id] as const,
  },

  deadlyBurger: {
    all: () => ['deadly-burger'] as const,
    lists: () => ['deadly-burger', 'list'] as const,
    detail: (id: string) => ['deadly-burger', id] as const,
  },

  interludes: {
    all: () => ['interludes'] as const,
    lists: () => ['interludes', 'list'] as const,
    detail: (id: string) => ['interludes', id] as const,
  },
} as const;
