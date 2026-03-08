import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const AdditionListPage = lazy(() =>
  import('@/pages/quiz/addition/AdditionListPage').then((m) => ({ default: m.AdditionListPage }))
);
const AdditionCreatePage = lazy(() =>
  import('@/pages/quiz/addition/AdditionCreatePage').then((m) => ({
    default: m.AdditionCreatePage,
  }))
);
const AdditionDetailPage = lazy(() =>
  import('@/pages/quiz/addition/AdditionDetailPage').then((m) => ({
    default: m.AdditionDetailPage,
  }))
);
const AdditionEditPage = lazy(() =>
  import('@/pages/quiz/addition/AdditionEditPage').then((m) => ({ default: m.AdditionEditPage }))
);

export const additionRoutes = createCrudRoutes('/addition', {
  List: AdditionListPage,
  Create: AdditionCreatePage,
  Detail: AdditionDetailPage,
  Edit: AdditionEditPage,
});
