import type { BurgerQuizDetail, BurgerQuizStructureElement } from '@/types';
import type { RoundSlug } from '@/features/quiz/constants/roundVisuals';

/**
 * Titre affiché d’une manche à partir d’un élément de structure (GET avec détail).
 * Pour un interlude vidéo, retourne `null` (titre géré ailleurs).
 */
export function getRoundTitleFromElement(
  el: BurgerQuizStructureElement | undefined
): string | null {
  if (!el) return null;
  switch (el.type) {
    case 'nuggets':
      return el.nuggets?.title ?? null;
    case 'salt_or_pepper':
      return el.salt_or_pepper?.title ?? null;
    case 'menus':
      return el.menus?.title ?? null;
    case 'addition':
      return el.addition?.title ?? null;
    case 'deadly_burger':
      return el.deadly_burger?.title ?? null;
    case 'video_interlude':
      return null;
    default:
      return null;
  }
}

/** Titre d’une manche identifiée par son slug dans le détail quiz. */
export function getRoundTitle(quiz: BurgerQuizDetail, slug: RoundSlug): string | null {
  const el = quiz.structure.find((e) => e.type === slug);
  return getRoundTitleFromElement(el);
}
