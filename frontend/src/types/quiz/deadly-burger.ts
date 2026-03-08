import type { Author, QuestionDetail } from './common';

export interface DeadlyBurgerDetail {
  id: string;
  title: string;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions: QuestionDetail[];
}

/* Payload create/update */
export interface DeadlyBurgerInput {
  title: string;
  original?: boolean;
  tags?: string[];
  question_ids?: string[];
}

export interface DeadlyBurgerListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}
