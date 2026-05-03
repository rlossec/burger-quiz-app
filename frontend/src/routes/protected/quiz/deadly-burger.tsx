import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const DeadlyBurgerListPage = lazy(() =>
  import('@/pages/quiz/deadly-burger/DeadlyBurgerListPage').then((m) => ({
    default: m.DeadlyBurgerListPage,
  }))
);
const DeadlyBurgerCreatePage = lazy(() =>
  import('@/pages/quiz/deadly-burger/DeadlyBurgerCreatePage').then((m) => ({
    default: m.DeadlyBurgerCreatePage,
  }))
);
const DeadlyBurgerDetailPage = lazy(() =>
  import('@/pages/quiz/deadly-burger/DeadlyBurgerDetailPage').then((m) => ({
    default: m.DeadlyBurgerDetailPage,
  }))
);
const DeadlyBurgerEditPage = lazy(() =>
  import('@/pages/quiz/deadly-burger/DeadlyBurgerEditPage').then((m) => ({
    default: m.DeadlyBurgerEditPage,
  }))
);

export const deadlyBurgerRoutes = createCrudRoutes('/deadly-burger', {
  List: DeadlyBurgerListPage,
  Create: DeadlyBurgerCreatePage,
  Detail: DeadlyBurgerDetailPage,
  Edit: DeadlyBurgerEditPage,
});
