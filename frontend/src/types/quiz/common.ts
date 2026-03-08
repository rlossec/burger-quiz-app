/**
 * Types partagés quiz — pagination, auteur, question/réponse.
 */

/* Réponse paginée standard Django REST. */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/* Auteur */
export interface Author {
  id: number;
  username: string;
}

/* Réponse */
export interface AnswerDetail {
  id: string;
  text: string;
  is_correct: boolean;
}

/* Question */
export interface QuestionDetail {
  id: string;
  text: string;
  question_type: string;
  original: boolean;
  explanations?: string;
  video_url?: string;
  image_url?: string;
  author?: Author;
  tags: string[];
  created_at: string;
  updated_at: string;
  answers: AnswerDetail[];
}
