import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { DeadlyBurgerInput, DeadlyBurgerListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { deadlyBurgerApi } from '../api/deadly-burger';

export function useDeadlyBurgerListQuery(params?: DeadlyBurgerListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.deadlyBurger.lists(), params] : queryKeys.deadlyBurger.lists(),
    queryFn: () => deadlyBurgerApi.list(params),
  });
}

export function useDeadlyBurgerDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.deadlyBurger.detail(id),
    queryFn: () => deadlyBurgerApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateDeadlyBurgerMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: deadlyBurgerApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.lists() });
      toast({ title: 'Deadly Burger créé avec succès' });
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

export function useUpdateDeadlyBurgerMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: DeadlyBurgerInput }) =>
      deadlyBurgerApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.lists() });
      toast({ title: 'Deadly Burger mis à jour avec succès' });
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

export function usePatchDeadlyBurgerMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<DeadlyBurgerInput> }) =>
      deadlyBurgerApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.lists() });
      toast({ title: 'Deadly Burger mis à jour avec succès' });
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

export function useDeleteDeadlyBurgerMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => deadlyBurgerApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.deadlyBurger.lists() });
      toast({ title: 'Deadly Burger supprimé avec succès' });
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
