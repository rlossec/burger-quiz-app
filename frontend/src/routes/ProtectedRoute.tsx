import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuthStore, selectIsAuthenticated, selectIsHydrated } from '@/stores';
import { Loader2 } from 'lucide-react';

export function ProtectedRoute() {
  const isAuthenticated = useAuthStore(selectIsAuthenticated);
  const isHydrated = useAuthStore(selectIsHydrated);
  const location = useLocation();

  if (!isHydrated) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="size-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!isAuthenticated) {
    const redirect = location.pathname + location.search;
    const to =
      redirect && redirect !== '/'
        ? { pathname: '/auth/login', search: `?redirect=${encodeURIComponent(redirect)}` }
        : '/auth/login';
    return <Navigate to={to} state={{ from: location }} replace />;
  }

  return <Outlet />;
}
