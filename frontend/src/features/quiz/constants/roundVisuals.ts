import type { LucideIcon } from 'lucide-react';
import { Beef, Film, FlaskRound, ReceiptText, Skull, UtensilsCrossed } from 'lucide-react';
import type { StructureElementSlug } from '@/types';

/** Types de manches (hors interlude vidéo). */
export type RoundSlug = Exclude<StructureElementSlug, 'video_interlude'>;

/** Ordre d’affichage / logique des manches dans l’UI. */
export const ROUND_SLUGS: readonly RoundSlug[] = [
  'nuggets',
  'salt_or_pepper',
  'menus',
  'addition',
  'deadly_burger',
] as const;

/**
 * Icônes + couleurs des manches (réutiliser partout dans le front quiz).
 * Les classes sont Tailwind ; ajuster ici pour unifier l’app.
 */
export interface RoundVisual {
  label: string;
  icon: LucideIcon;
  iconClassName: string;
  iconBgClassName: string;
}

export const ROUND_VISUALS: Record<RoundSlug, RoundVisual> = {
  nuggets: {
    label: 'Nuggets',
    icon: Beef,
    iconClassName: 'text-orange-500',
    iconBgClassName: 'bg-orange-500/15',
  },
  salt_or_pepper: {
    label: 'Sel ou Poivre',
    icon: FlaskRound,
    iconClassName: 'text-slate-400',
    iconBgClassName: 'bg-slate-500/15',
  },
  menus: {
    label: 'Menus',
    icon: UtensilsCrossed,
    iconClassName: 'text-violet-500',
    iconBgClassName: 'bg-violet-500/15',
  },
  addition: {
    label: 'Addition',
    icon: ReceiptText,
    iconClassName: 'text-emerald-600 dark:text-emerald-400',
    iconBgClassName: 'bg-emerald-500/15',
  },
  deadly_burger: {
    label: 'Burger de la mort',
    icon: Skull,
    iconClassName: 'text-red-500',
    iconBgClassName: 'bg-red-500/15',
  },
};

/** Interlude : pas dans ROUND_VISUALS (type distinct). */
export const VIDEO_INTERLUDE_VISUAL: Omit<RoundVisual, 'label'> & { label: string } = {
  label: 'Interlude',
  icon: Film,
  iconClassName: 'text-muted-foreground',
  iconBgClassName: 'bg-muted',
};

export function getRoundVisual(slug: RoundSlug): RoundVisual {
  return ROUND_VISUALS[slug];
}
