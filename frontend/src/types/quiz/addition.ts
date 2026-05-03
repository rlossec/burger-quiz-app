import type { Author, QuestionDetail } from './common';

export interface AdditionDetail {
  id: string;
  title: string;
  description: string | null;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions: QuestionDetail[];
}

/* Payload create/update */
export interface AdditionInput {
  title: string;
  description?: string;
  original?: boolean;
  tags?: string[];
  question_ids?: string[];
}

export interface AdditionListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}
