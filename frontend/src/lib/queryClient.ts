import { QueryClient, MutationCache, QueryCache } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { getApiErrorMessage } from './api-error';

// ─── QueryClient ───────────────────────────────────────────────────────────────

export const queryClient = new QueryClient({
  // Gestion globale des erreurs de queries
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Log uniquement si la query a déjà des données (erreur en background)
      if (query.state.data !== undefined) {
        console.error(
          `[QueryCache] Erreur en background sur "${String(query.queryKey[0])}" :`,
          getApiErrorMessage(error)
        );
      }
    },
  }),

  // Gestion globale des erreurs de mutations
  mutationCache: new MutationCache({
    onError: (error) => {
      console.error('[MutationCache] Erreur :', getApiErrorMessage(error));
    },
  }),

  defaultOptions: {
    queries: {
      // Durée pendant laquelle les données sont considérées "fraîches"
      staleTime: 1000 * 60 * 5, // 5 minutes

      // Durée de conservation en cache après démontage du composant
      gcTime: 1000 * 60 * 10, // 10 minutes (anciennement cacheTime)

      // Ne pas relancer la query au focus de la fenêtre en dev
      refetchOnWindowFocus: import.meta.env.PROD,

      // 2 tentatives max avant d'afficher l'erreur
      retry: (failureCount, error) => {
        // Pas de retry sur les erreurs 4xx (client)
        if (error instanceof AxiosError) {
          const status = error.response?.status;
          if (status && status >= 400 && status < 500) return false;
        }
        return failureCount < 2;
      },
    },
    mutations: {
      // Pas de retry automatique sur les mutations
      retry: false,
    },
  },
});
