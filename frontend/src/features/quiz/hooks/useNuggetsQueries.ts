import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { NuggetsInput, NuggetsListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { nuggetsApi } from '../api/nuggets';

export function useNuggetsListQuery(params?: NuggetsListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.nuggets.lists(), params] : queryKeys.nuggets.lists(),
    queryFn: () => nuggetsApi.list(params),
  });
}

export function useNuggetsDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.nuggets.detail(id),
    queryFn: () => nuggetsApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateNuggetsMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: nuggetsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.lists() });
      toast({ title: 'Nuggets créés avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la création des nuggets',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateNuggetsMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: NuggetsInput }) =>
      nuggetsApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.lists() });
      toast({ title: 'Nuggets mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour des nuggets',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function usePatchNuggetsMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<NuggetsInput> }) =>
      nuggetsApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.lists() });
      toast({ title: 'Nuggets mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour des nuggets',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteNuggetsMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => nuggetsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.nuggets.lists() });
      toast({ title: 'Nuggets supprimés avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la suppression des nuggets',
        description: getApiErrorMessage(error),
      });
    },
  });
}
