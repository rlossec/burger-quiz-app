import { Loader2 } from 'lucide-react';

/**
 * Fallback unique pour le Suspense racine (lazy loading des routes).
 * Réutilisable partout où on a besoin d'un chargement de page plein écran.
 */
export function PageLoader() {
  return (
    <div className="flex min-h-screen items-center justify-center" aria-label="Chargement">
      <Loader2 className="size-10 animate-spin text-primary" />
    </div>
  );
}
