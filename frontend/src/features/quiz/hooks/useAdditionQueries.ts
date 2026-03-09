import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { AdditionInput, AdditionListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { additionApi } from '../api/addition';

export function useAdditionListQuery(params?: AdditionListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.addition.lists(), params] : queryKeys.addition.lists(),
    queryFn: () => additionApi.list(params),
  });
}

export function useAdditionDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.addition.detail(id),
    queryFn: () => additionApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateAdditionMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: additionApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.lists() });
      toast({ title: 'Addition créée avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la création',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateAdditionMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: AdditionInput }) =>
      additionApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.lists() });
      toast({ title: 'Addition mise à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function usePatchAdditionMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<AdditionInput> }) =>
      additionApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.lists() });
      toast({ title: 'Addition mise à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteAdditionMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => additionApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.addition.lists() });
      toast({ title: 'Addition supprimée avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la suppression',
        description: getApiErrorMessage(error),
      });
    },
  });
}
