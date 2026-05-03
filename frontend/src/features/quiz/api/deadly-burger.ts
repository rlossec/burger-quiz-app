import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  DeadlyBurgerDetail,
  DeadlyBurgerInput,
  DeadlyBurgerListParams,
} from '@/types';

export const deadlyBurgerApi = {
  list: async (params?: DeadlyBurgerListParams): Promise<PaginatedResponse<DeadlyBurgerDetail>> => {
    const { data } = await apiClient.get('/quiz/deadly-burgers/', { params });
    return data;
  },

  detail: async (id: string): Promise<DeadlyBurgerDetail> => {
    const { data } = await apiClient.get(`/quiz/deadly-burgers/${id}/`);
    return data;
  },

  create: async (payload: DeadlyBurgerInput): Promise<DeadlyBurgerDetail> => {
    const { data } = await apiClient.post('/quiz/deadly-burgers/', payload);
    return data;
  },

  update: async (id: string, payload: DeadlyBurgerInput): Promise<DeadlyBurgerDetail> => {
    const { data } = await apiClient.put(`/quiz/deadly-burgers/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<DeadlyBurgerInput>): Promise<DeadlyBurgerDetail> => {
    const { data } = await apiClient.patch(`/quiz/deadly-burgers/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/deadly-burgers/${id}/`);
  },
} as const;
