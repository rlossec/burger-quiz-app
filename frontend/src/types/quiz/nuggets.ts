import type { Author, QuestionDetail } from './common';

export interface NuggetsDetail {
  id: string;
  title: string;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  questions: QuestionDetail[];
}

/** Payload create/update. */
export interface NuggetsInput {
  title: string;
  original?: boolean;
  tags?: string[];
  question_ids?: string[];
}

export interface NuggetsListParams {
  search?: string;
  tags?: string[];
  page?: number;
  page_size?: number;
  ordering?: string;
}
