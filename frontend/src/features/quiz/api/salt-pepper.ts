import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  SaltPepperDetail,
  SaltPepperInput,
  SaltPepperListParams,
} from '@/types';

export const saltPepperApi = {
  list: async (params?: SaltPepperListParams): Promise<PaginatedResponse<SaltPepperDetail>> => {
    const { data } = await apiClient.get('/quiz/salt-or-pepper/', { params });
    return data;
  },

  detail: async (id: string): Promise<SaltPepperDetail> => {
    const { data } = await apiClient.get(`/quiz/salt-or-pepper/${id}/`);
    return data;
  },

  create: async (payload: SaltPepperInput): Promise<SaltPepperDetail> => {
    const { data } = await apiClient.post('/quiz/salt-or-pepper/', payload);
    return data;
  },

  update: async (id: string, payload: SaltPepperInput): Promise<SaltPepperDetail> => {
    const { data } = await apiClient.put(`/quiz/salt-or-pepper/${id}/`, payload);
    return data;
  },

  patch: async (id: string, payload: Partial<SaltPepperInput>): Promise<SaltPepperDetail> => {
    const { data } = await apiClient.patch(`/quiz/salt-or-pepper/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/salt-or-pepper/${id}/`);
  },
} as const;
