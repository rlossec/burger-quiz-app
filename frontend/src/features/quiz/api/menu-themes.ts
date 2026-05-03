import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  MenuThemeDetail,
  MenuThemeInput,
  MenuThemeListParams,
} from '@/types';

export const menuThemesApi = {
  list: async (params?: MenuThemeListParams): Promise<PaginatedResponse<MenuThemeDetail>> => {
    const { data } = await apiClient.get('/quiz/menu-themes/', { params });
    return data;
  },

  detail: async (id: string): Promise<MenuThemeDetail> => {
    const { data } = await apiClient.get(`/quiz/menu-themes/${id}/`);
    return data;
  },

  create: async (payload: MenuThemeInput): Promise<MenuThemeDetail> => {
    const { data } = await apiClient.post('/quiz/menu-themes/', payload);
    return data;
  },

  update: async (id: string, payload: MenuThemeInput): Promise<MenuThemeDetail> => {
    const { data } = await apiClient.put(`/quiz/menu-themes/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<MenuThemeInput>): Promise<MenuThemeDetail> => {
    const { data } = await apiClient.patch(`/quiz/menu-themes/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/menu-themes/${id}/`);
  },
} as const;
