import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  VideoInterludeDetail,
  VideoInterludeInput,
  VideoInterludeListParams,
  VideoInterludeListItem,
} from '@/types';

export const interludesApi = {
  list: async (
    params?: VideoInterludeListParams
  ): Promise<PaginatedResponse<VideoInterludeListItem>> => {
    const { data } = await apiClient.get('/quiz/interludes/', { params });
    return data;
  },

  detail: async (id: string): Promise<VideoInterludeDetail> => {
    const { data } = await apiClient.get(`/quiz/interludes/${id}/`);
    return data;
  },

  create: async (payload: VideoInterludeInput): Promise<VideoInterludeDetail> => {
    const { data } = await apiClient.post('/quiz/interludes/', payload);
    return data;
  },

  update: async (id: string, payload: VideoInterludeInput): Promise<VideoInterludeDetail> => {
    const { data } = await apiClient.put(`/quiz/interludes/${id}/`, payload);
    return data;
  },

  patch: async (
    id: string,
    payload: Partial<VideoInterludeInput>
  ): Promise<VideoInterludeDetail> => {
    const { data } = await apiClient.patch(`/quiz/interludes/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/interludes/${id}/`);
  },
} as const;
