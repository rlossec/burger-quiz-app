import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { MenusInput, MenusListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { menusApi } from '../api/menus';

export function useMenusListQuery(params?: MenusListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.menus.lists(), params] : queryKeys.menus.lists(),
    queryFn: () => menusApi.list(params),
  });
}

export function useMenusDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.menus.detail(id),
    queryFn: () => menusApi.detail(id),
    enabled: !!id,
  });
}

export function useCreateMenusMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: menusApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.lists() });
      toast({ title: 'Menu créé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la création du menu',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateMenusMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: MenusInput }) =>
      menusApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.lists() });
      toast({ title: 'Menu mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour du menu',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function usePatchMenusMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<MenusInput> }) =>
      menusApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.lists() });
      toast({ title: 'Menu mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour du menu',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteMenusMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => menusApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menus.lists() });
      toast({ title: 'Menu supprimé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la suppression du menu',
        description: getApiErrorMessage(error),
      });
    },
  });
}
