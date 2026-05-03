import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const NuggetsListPage = lazy(() =>
  import('@/pages/quiz/nuggets/NuggetsListPage').then((m) => ({ default: m.NuggetsListPage }))
);
const NuggetsCreatePage = lazy(() =>
  import('@/pages/quiz/nuggets/NuggetsCreatePage').then((m) => ({ default: m.NuggetsCreatePage }))
);
const NuggetsDetailPage = lazy(() =>
  import('@/pages/quiz/nuggets/NuggetsDetailPage').then((m) => ({ default: m.NuggetsDetailPage }))
);
const NuggetsEditPage = lazy(() =>
  import('@/pages/quiz/nuggets/NuggetsEditPage').then((m) => ({
    default: m.NuggetsEditPage,
  }))
);

export const nuggetsRoutes = createCrudRoutes('/nuggets', {
  List: NuggetsListPage,
  Create: NuggetsCreatePage,
  Detail: NuggetsDetailPage,
  Edit: NuggetsEditPage,
});
