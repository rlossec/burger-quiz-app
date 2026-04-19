import type { Author } from './common';

/** Réponse détail — VideoInterludeSerializer. */
export interface VideoInterludeDetail {
  id: string;
  title: string;
  youtube_url: string;
  youtube_video_id: string;
  duration_seconds: number | null;
  autoplay: boolean;
  skip_allowed: boolean;
  skip_after_seconds: number | null;
  author: Author | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

/** Liste — VideoInterludeListSerializer (sans auteur ni tags). */
export interface VideoInterludeListItem {
  id: string;
  title: string;
  youtube_url: string;
  youtube_video_id: string;
  duration_seconds: number | null;
  autoplay: boolean;
  skip_allowed: boolean;
  skip_after_seconds: number | null;
  created_at: string;
  updated_at: string;
}

/** Payload create/update — VideoInterludeSerializer (youtube_video_id en lecture seule). */
export interface VideoInterludeInput {
  title: string;
  youtube_url: string;
  duration_seconds?: number | null;
  autoplay?: boolean;
  skip_allowed?: boolean;
  skip_after_seconds?: number | null;
  tags?: string[];
}

/** Query liste — filtres `tag`, `search`. */
export interface VideoInterludeListParams {
  tag?: string;
  search?: string;
  page?: number;
  page_size?: number;
  ordering?: string;
}
