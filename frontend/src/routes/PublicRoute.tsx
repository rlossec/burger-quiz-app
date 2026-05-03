import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore, selectIsAuthenticated, selectIsHydrated } from '@/stores';

/**
 * Guard pour les routes publiques (login, register).
 * Redirige vers le dashboard si l'utilisateur est déjà connecté.
 */
export function PublicRoute() {
  const isAuthenticated = useAuthStore(selectIsAuthenticated);
  const isHydrated = useAuthStore(selectIsHydrated);

  if (!isHydrated) {
    return null; // ou un loader
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
