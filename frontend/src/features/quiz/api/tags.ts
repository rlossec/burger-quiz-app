import { apiClient } from '@/lib/axios';

interface TagCatalogResponse {
  results: string[];
}

export const tagsApi = {
  catalog: async (limit = 100): Promise<string[]> => {
    const { data } = await apiClient.get<TagCatalogResponse>('/quiz/tags/', {
      params: { limit },
    });
    return data.results ?? [];
  },
} as const;
