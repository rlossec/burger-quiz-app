import { Menu, X } from 'lucide-react';
import { cn } from '@/lib/utils';

type MobileMenuToggleProps = {
  open: boolean;
  onToggle: () => void;
  className?: string;
};

/**
 * Bouton hamburger / X pour ouvrir/fermer le menu mobile.
 */
export function MobileMenuToggle({ open, onToggle, className }: MobileMenuToggleProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      className={cn(
        'flex h-10 w-10 items-center justify-center rounded-lg transition-colors md:hidden',
        'bg-cream/10 text-cream hover:bg-cream/20',
        className
      )}
      aria-label={open ? 'Fermer le menu' : 'Ouvrir le menu'}
    >
      {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
    </button>
  );
}
