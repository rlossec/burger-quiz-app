import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { SaltPepperInput, SaltPepperListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { saltPepperApi } from '../api/salt-pepper';

export function useSaltPepperListQuery(params?: SaltPepperListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.saltPepper.lists(), params] : queryKeys.saltPepper.lists(),
    queryFn: () => saltPepperApi.list(params),
  });
}

export function useSaltPepperDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.saltPepper.detail(id),
    queryFn: () => saltPepperApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateSaltPepperMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: saltPepperApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.lists() });
      toast({ title: 'Salt & Pepper créé avec succès' });
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

export function useUpdateSaltPepperMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: SaltPepperInput }) =>
      saltPepperApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.lists() });
      toast({ title: 'Salt & Pepper mis à jour avec succès' });
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

export function usePatchSaltPepperMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<SaltPepperInput> }) =>
      saltPepperApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.lists() });
      toast({ title: 'Salt & Pepper mis à jour avec succès' });
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

export function useDeleteSaltPepperMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => saltPepperApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.saltPepper.lists() });
      toast({ title: 'Salt & Pepper supprimé avec succès' });
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
