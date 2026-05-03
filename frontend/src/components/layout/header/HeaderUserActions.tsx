import { Link } from 'react-router-dom';
import { User, LogOut } from 'lucide-react';

type Variant = 'desktop' | 'mobile';

type HeaderUserActionsProps = {
  username?: string | null;
  onLogout: () => void;
  variant: Variant;
  onNavigate?: () => void;
};

/**
 * Actions utilisateur dans le header : lien profil + déconnexion.
 * - desktop : affichage compact (icône seule pour déco)
 * - mobile : affichage empilé avec texte "Déconnexion"
 */
export function HeaderUserActions({
  username,
  onLogout,
  variant,
  onNavigate,
}: HeaderUserActionsProps) {
  const linkClass =
    'inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-cream/80 transition-colors hover:bg-denim/20 hover:text-denim';
  const buttonClass =
    'inline-flex items-center gap-2 rounded-md text-cream/80 transition-colors hover:bg-ketchup/20 hover:text-ketchup';

  if (variant === 'desktop') {
    return (
      <div className="hidden items-center gap-2 md:flex">
        <Link to="/profile" className={linkClass}>
          <User className="h-4 w-4" />
          {username || 'Profil'}
        </Link>
        <button
          onClick={onLogout}
          title="Déconnexion"
          className={`inline-flex h-9 w-9 items-center justify-center rounded-md ${buttonClass}`}
        >
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      <Link to="/profile" onClick={onNavigate} className={linkClass}>
        <User className="h-4 w-4" />
        {username || 'Mon profil'}
      </Link>
      <button onClick={onLogout} className={`w-full px-3 py-2 text-left rounded-md ${buttonClass}`}>
        <LogOut className="h-4 w-4" />
        Déconnexion
      </button>
    </div>
  );
}
