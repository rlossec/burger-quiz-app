import { apiClient } from '@/lib/axios';
import type { PaginatedResponse, AdditionDetail, AdditionInput, AdditionListParams } from '@/types';

export const additionApi = {
  list: async (params?: AdditionListParams): Promise<PaginatedResponse<AdditionDetail>> => {
    const { data } = await apiClient.get('/quiz/additions/', { params });
    return data;
  },

  detail: async (id: string): Promise<AdditionDetail> => {
    const { data } = await apiClient.get(`/quiz/additions/${id}/`);
    return data;
  },

  create: async (payload: AdditionInput): Promise<AdditionDetail> => {
    const { data } = await apiClient.post('/quiz/additions/', payload);
    return data;
  },

  update: async (id: string, payload: AdditionInput): Promise<AdditionDetail> => {
    const { data } = await apiClient.put(`/quiz/additions/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<AdditionInput>): Promise<AdditionDetail> => {
    const { data } = await apiClient.patch(`/quiz/additions/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/additions/${id}/`);
  },
} as const;
