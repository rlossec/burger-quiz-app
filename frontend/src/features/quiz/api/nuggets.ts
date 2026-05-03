import { apiClient } from '@/lib/axios';
import type { PaginatedResponse, NuggetsDetail, NuggetsInput, NuggetsListParams } from '@/types';

export const nuggetsApi = {
  list: async (params?: NuggetsListParams): Promise<PaginatedResponse<NuggetsDetail>> => {
    const { data } = await apiClient.get('/quiz/nuggets/', { params });
    return data;
  },

  detail: async (id: string): Promise<NuggetsDetail> => {
    const { data } = await apiClient.get(`/quiz/nuggets/${id}/`);
    return data;
  },

  create: async (payload: NuggetsInput): Promise<NuggetsDetail> => {
    const { data } = await apiClient.post('/quiz/nuggets/', payload);
    return data;
  },

  update: async (id: string, payload: NuggetsInput): Promise<NuggetsDetail> => {
    const { data } = await apiClient.put(`/quiz/nuggets/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<NuggetsInput>): Promise<NuggetsDetail> => {
    const { data } = await apiClient.patch(`/quiz/nuggets/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/nuggets/${id}/`);
  },
} as const;
