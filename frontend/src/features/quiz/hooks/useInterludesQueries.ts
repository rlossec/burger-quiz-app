import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { InterludeInput, InterludeListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { interludesApi } from '../api/interludes';

export function useInterludesListQuery(params?: InterludeListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.interludes.lists(), params] : queryKeys.interludes.lists(),
    queryFn: () => interludesApi.list(params),
  });
}

export function useInterludesDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.interludes.detail(id),
    queryFn: () => interludesApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateInterludesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: interludesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.lists() });
      toast({ title: 'Interlude créé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: "Erreur lors de la création de l'interlude",
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateInterludesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: InterludeInput }) =>
      interludesApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.lists() });
      toast({ title: 'Interlude mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: "Erreur lors de la mise à jour de l'interlude",
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function usePatchInterludesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<InterludeInput> }) =>
      interludesApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.lists() });
      toast({ title: 'Interlude mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: "Erreur lors de la mise à jour de l'interlude",
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteInterludesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => interludesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.interludes.lists() });
      toast({ title: 'Interlude supprimé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: "Erreur lors de la suppression de l'interlude",
        description: getApiErrorMessage(error),
      });
    },
  });
}
