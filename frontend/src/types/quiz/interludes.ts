import type { Author } from './common';

/** Type d'interlude vidéo — InterludeType. */
export type InterludeType = 'IN' | 'OU' | 'PU' | 'IL';

export interface InterludeDetail {
  id: string;
  title: string;
  youtube_url: string;
  youtube_video_id: string;
  interlude_type: InterludeType;
  duration_seconds: number | null;
  autoplay: boolean;
  skip_allowed: boolean;
  skip_after_seconds: number | null;
  created_at: string;
  updated_at: string;
  author?: Author | null;
  tags?: string[];
}

/* Payload create/update */
export interface InterludeInput {
  title: string;
  youtube_url: string;
  interlude_type?: InterludeType;
  duration_seconds?: number | null;
  autoplay?: boolean;
  skip_allowed?: boolean;
  skip_after_seconds?: number | null;
  tags?: string[];
}

export interface InterludeListParams {
  search?: string;
  interlude_type?: InterludeType;
  page?: number;
  page_size?: number;
  ordering?: string;
}
