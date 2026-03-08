import type { Author, QuestionDetail } from './common';

export interface SaltPepperDetail {
  id: string;
  title: string;
  description: string | null;
  original: boolean;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
  propositions: string[];
  questions: QuestionDetail[];
}

/** Payload create/update */
export interface SaltPepperInput {
  title: string;
  description?: string;
  original?: boolean;
  tags?: string[];
  propositions: string[];
  question_ids?: string[];
}

export interface SaltPepperListParams {
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}
