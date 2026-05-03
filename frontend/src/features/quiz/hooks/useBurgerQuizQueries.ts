import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { BurgerQuizInput, BurgerQuizListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { quizApi } from '../api/quiz';

export function useBurgerQuizListQuery(params?: BurgerQuizListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.quiz.lists(), params] : queryKeys.quiz.lists(),
    queryFn: () => quizApi.list(params),
  });
}

export function useBurgerQuizDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.quiz.detail(id),
    queryFn: () => quizApi.detail(id),
    enabled: !!id,
  });
}

export function useBurgerQuizStructureQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.quiz.structure(id),
    queryFn: () => quizApi.structure(id),
    enabled: !!id,
  });
}

export function useCreateBurgerQuizMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: quizApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.quiz.lists() });
      toast({ title: 'Quiz créé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la création du quiz',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateBurgerQuizMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: BurgerQuizInput }) =>
      quizApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.quiz.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.quiz.structure(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.quiz.lists() });
      toast({ title: 'Quiz mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour du quiz',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteBurgerQuizMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => quizApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.quiz.lists() });
      toast({ title: 'Quiz supprimé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la suppression du quiz',
        description: getApiErrorMessage(error),
      });
    },
  });
}
