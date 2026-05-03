import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  InterludeDetail,
  InterludeInput,
  InterludeListParams,
} from '@/types';

export const interludesApi = {
  list: async (params?: InterludeListParams): Promise<PaginatedResponse<InterludeDetail>> => {
    const { data } = await apiClient.get('/quiz/interludes/', { params });
    return data;
  },

  detail: async (id: string): Promise<InterludeDetail> => {
    const { data } = await apiClient.get(`/quiz/interludes/${id}/`);
    return data;
  },

  create: async (payload: InterludeInput): Promise<InterludeDetail> => {
    const { data } = await apiClient.post('/quiz/interludes/', payload);
    return data;
  },

  update: async (id: string, payload: InterludeInput): Promise<InterludeDetail> => {
    const { data } = await apiClient.put(`/quiz/interludes/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<InterludeInput>): Promise<InterludeDetail> => {
    const { data } = await apiClient.patch(`/quiz/interludes/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/interludes/${id}/`);
  },
} as const;
