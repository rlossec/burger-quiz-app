import type { Author, QuestionDetail } from './common';

/** Type de thème menu — MENU_TYPES. */
export type MenuThemeType = 'CL' | 'TR';

export interface MenuThemeDetail {
  id: string;
  title: string;
  type: MenuThemeType;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions: QuestionDetail[];
}

/* Payload create/update. */
export interface MenuThemeInput {
  title: string;
  type: MenuThemeType;
  original?: boolean;
  tags?: string[];
  question_ids?: string[];
}

export interface MenuThemeListParams {
  type?: MenuThemeType;
  page?: number;
  page_size?: number;
  ordering?: string;
}
