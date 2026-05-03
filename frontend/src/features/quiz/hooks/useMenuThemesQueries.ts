import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';
import { getApiErrorMessage } from '@/lib/api-error';
import type { MenuThemeInput, MenuThemeListParams } from '@/types';
import { queryKeys } from '../api/query-keys';
import { menuThemesApi } from '../api/menu-themes';

export function useMenuThemesListQuery(params?: MenuThemeListParams) {
  return useQuery({
    queryKey: params ? [...queryKeys.menuThemes.lists(), params] : queryKeys.menuThemes.lists(),
    queryFn: () => menuThemesApi.list(params),
  });
}

export function useMenuThemesDetailQuery(id: string) {
  return useQuery({
    queryKey: queryKeys.menuThemes.detail(id),
    queryFn: () => menuThemesApi.detail(id),
    enabled: !!id,
  });
}

export function useMenuThemesByTypeQuery(type: 'CL' | 'TR') {
  return useQuery({
    queryKey: queryKeys.menuThemes.byType(type),
    queryFn: () => menuThemesApi.list({ type }),
  });
}

export function useCreateMenuThemesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: menuThemesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.all() });
      toast({ title: 'Thème de menu créé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la création du thème',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useUpdateMenuThemesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: MenuThemeInput }) =>
      menuThemesApi.update(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.all() });
      toast({ title: 'Thème de menu mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour du thème',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function usePatchMenuThemesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<MenuThemeInput> }) =>
      menuThemesApi.patch(id, payload),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.all() });
      toast({ title: 'Thème de menu mis à jour avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la mise à jour du thème',
        description: getApiErrorMessage(error),
      });
    },
  });
}

export function useDeleteMenuThemesMutation() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: (id: string) => menuThemesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.menuThemes.all() });
      toast({ title: 'Thème de menu supprimé avec succès' });
    },
    onError: (error) => {
      toast({
        variant: 'destructive',
        title: 'Erreur lors de la suppression du thème',
        description: getApiErrorMessage(error),
      });
    },
  });
}
