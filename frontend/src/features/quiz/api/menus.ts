import { apiClient } from '@/lib/axios';
import type { PaginatedResponse, MenusDetail, MenusInput, MenusListParams } from '@/types';

export const menusApi = {
  list: async (params?: MenusListParams): Promise<PaginatedResponse<MenusDetail>> => {
    const { data } = await apiClient.get('/quiz/menus/', { params });
    return data;
  },

  detail: async (id: string): Promise<MenusDetail> => {
    const { data } = await apiClient.get(`/quiz/menus/${id}/`);
    return data;
  },

  create: async (payload: MenusInput): Promise<MenusDetail> => {
    const { data } = await apiClient.post('/quiz/menus/', payload);
    return data;
  },

  update: async (id: string, payload: MenusInput): Promise<MenusDetail> => {
    const { data } = await apiClient.put(`/quiz/menus/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<MenusInput>): Promise<MenusDetail> => {
    const { data } = await apiClient.patch(`/quiz/menus/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/menus/${id}/`);
  },
} as const;
