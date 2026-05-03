import type { Author } from './common';
import type { NuggetsDetail } from './nuggets';
import type { SaltPepperDetail } from './salt-pepper';
import type { MenusDetail } from './menus';
import type { AdditionDetail } from './addition';
import type { DeadlyBurgerDetail } from './deadly-burger';
import type { InterludeType } from './interludes';

export interface BurgerQuizDetail {
  id: string;
  title: string;
  toss: string;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  nuggets: NuggetsDetail | null;
  salt_or_pepper: SaltPepperDetail | null;
  menus: MenusDetail | null;
  addition: AdditionDetail | null;
  deadly_burger: DeadlyBurgerDetail | null;
}

/* Payload create/update */
export interface BurgerQuizInput {
  title: string;
  toss: string;
  tags?: string[];
  nuggets_id?: string | null;
  salt_or_pepper_id?: string | null;
  menus_id?: string | null;
  addition_id?: string | null;
  deadly_burger_id?: string | null;
}

export interface BurgerQuizListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}

/* Structure */
export type RoundType = 'NU' | 'SP' | 'ME' | 'AD' | 'DB';
export type ElementType = 'round' | 'interlude';

export interface BurgerQuizStructureInterlude {
  id: string;
  title: string;
  interlude_type: InterludeType;
  youtube_video_id: string;
}

export interface BurgerQuizStructureElement {
  order: number;
  element_type: ElementType;
  round_type: RoundType | null;
  interlude: BurgerQuizStructureInterlude | null;
}

export interface BurgerQuizStructureResponse {
  burger_quiz_id: string;
  elements: BurgerQuizStructureElement[];
}
