import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  BurgerQuizDetail,
  BurgerQuizInput,
  BurgerQuizListParams,
  BurgerQuizStructureResponse,
} from '@/types';

export const quizApi = {
  list: async (params?: BurgerQuizListParams): Promise<PaginatedResponse<BurgerQuizDetail>> => {
    const { data } = await apiClient.get('/quiz/burger-quizzes/', { params });
    return data;
  },

  detail: async (id: string): Promise<BurgerQuizDetail> => {
    const { data } = await apiClient.get(`/quiz/burger-quizzes/${id}/`);
    return data;
  },

  create: async (payload: BurgerQuizInput): Promise<BurgerQuizDetail> => {
    const { data } = await apiClient.post('/quiz/burger-quizzes/', payload);
    return data;
  },

  update: async (id: string, payload: BurgerQuizInput): Promise<BurgerQuizDetail> => {
    const { data } = await apiClient.put(`/quiz/burger-quizzes/${id}/`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/quiz/burger-quizzes/${id}/`);
  },

  structure: async (id: string): Promise<BurgerQuizStructureResponse> => {
    const { data } = await apiClient.get(`/quiz/burger-quizzes/${id}/structure/`);
    return data;
  },
} as const;
