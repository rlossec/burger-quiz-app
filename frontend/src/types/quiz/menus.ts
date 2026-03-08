import type { Author } from './common';
import type { MenuThemeDetail } from './menu-theme';

export interface MenusDetail {
  id: string;
  title: string;
  description: string | null;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  menu_1: MenuThemeDetail | null;
  menu_2: MenuThemeDetail | null;
  menu_troll: MenuThemeDetail | null;
}

/** Payload create/update */
export interface MenusInput {
  title: string;
  description?: string;
  original?: boolean;
  tags?: string[];
  menu_1_id?: string;
  menu_2_id?: string;
  menu_troll_id?: string;
}

export interface MenusListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}
