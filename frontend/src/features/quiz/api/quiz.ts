import { apiClient } from '@/lib/axios';
import type {
  PaginatedResponse,
  BurgerQuizDetail,
  BurgerQuizInput,
  BurgerQuizListParams,
  BurgerQuizStructurePutPayload,
  BurgerQuizStructureResponse,
} from '@/types';

export const quizApi = {
  list: async (params?: BurgerQuizListParams): Promise<PaginatedResponse<BurgerQuizDetail>> => {
    const { data } = await apiClient.get('/quiz/burger-quizzes/', { params });
    return data;
  },

  detail: async (id: string): Promise<BurgerQuizDetail> => {
    const { data } = await apiClient.get(`/quiz/burger-quizzes/${id}/`, {
      params: { expand: 'full' },
    });
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

  updateStructure: async (
    id: string,
    payload: BurgerQuizStructurePutPayload
  ): Promise<BurgerQuizStructureResponse> => {
    const { data } = await apiClient.put(`/quiz/burger-quizzes/${id}/structure/`, payload);
    return data;
  },
} as const;
