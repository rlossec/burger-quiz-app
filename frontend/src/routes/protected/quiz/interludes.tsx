import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const InterludesListPage = lazy(() =>
  import('@/pages/quiz/interludes/InterludesListPage').then((m) => ({
    default: m.InterludesListPage,
  }))
);
const InterludesCreatePage = lazy(() =>
  import('@/pages/quiz/interludes/InterludesCreatePage').then((m) => ({
    default: m.InterludesCreatePage,
  }))
);
const InterludesDetailPage = lazy(() =>
  import('@/pages/quiz/interludes/InterludesDetailPage').then((m) => ({
    default: m.InterludesDetailPage,
  }))
);
const InterludesEditPage = lazy(() =>
  import('@/pages/quiz/interludes/InterludesEditPage').then((m) => ({
    default: m.InterludesEditPage,
  }))
);

export const interludesRoutes = createCrudRoutes('/interludes', {
  List: InterludesListPage,
  Create: InterludesCreatePage,
  Detail: InterludesDetailPage,
  Edit: InterludesEditPage,
});
