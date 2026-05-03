import { useQuery } from '@tanstack/react-query';
import { queryKeys } from '../api/query-keys';
import { tagsApi } from '../api/tags';

export function useTagCatalog() {
  return useQuery({
    queryKey: queryKeys.tags.catalog(),
    queryFn: () => tagsApi.catalog(100),
    staleTime: 1000 * 60 * 15,
  });
}
