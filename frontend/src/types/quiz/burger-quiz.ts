import type { Author } from './common';
import type { NuggetsDetail } from './nuggets';
import type { SaltPepperDetail } from './salt-pepper';
import type { MenusDetail } from './menus';
import type { AdditionDetail } from './addition';
import type { DeadlyBurgerDetail } from './deadly-burger';
import type { VideoInterludeDetail } from './interludes';

export interface BurgerQuizDetail {
  id: string;
  title: string;
  toss: string;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  /**
   * Ordre des manches et interludes.
   * Sans `?expand=full` : seulement `order`, `type`, `id`.
   * Avec `expand=full` ou GET `/structure/` : détail sous la clé du `type`.
   */
  structure: BurgerQuizStructureElement[];
}

/** Payload create/update — BurgerQuizSerializer (hors structure, gérée par PUT /structure/). */
export interface BurgerQuizInput {
  title: string;
  toss: string;
  tags?: string[];
}

export interface BurgerQuizListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}

/** Structure d'un Burger Quiz */

/** Slug API aligné sur `STRUCTURE_TYPE_TO_MODEL` (backend). */
export type StructureElementSlug =
  | 'nuggets'
  | 'salt_or_pepper'
  | 'menus'
  | 'addition'
  | 'deadly_burger'
  | 'video_interlude';

/**
 * GET détail (`structure`) ou GET `/structure/`.
 */
export interface BurgerQuizStructureElement {
  order: number;
  type: StructureElementSlug;
  id: string;
  nuggets?: NuggetsDetail;
  salt_or_pepper?: SaltPepperDetail;
  menus?: MenusDetail;
  addition?: AdditionDetail;
  deadly_burger?: DeadlyBurgerDetail;
  video_interlude?: VideoInterludeDetail;
}

export interface BurgerQuizStructureResponse {
  burger_quiz_id: string;
  elements: BurgerQuizStructureElement[];
}

/** PUT `/structure/` */
export interface BurgerQuizStructureElementWrite {
  type: StructureElementSlug;
  id: string;
}

export interface BurgerQuizStructurePutPayload {
  elements: BurgerQuizStructureElementWrite[];
}
