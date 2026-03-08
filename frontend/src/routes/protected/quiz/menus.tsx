import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const MenusListPage = lazy(() =>
  import('@/pages/quiz/menus/MenusListPage').then((m) => ({ default: m.MenusListPage }))
);
const MenusCreatePage = lazy(() =>
  import('@/pages/quiz/menus/MenusCreatePage').then((m) => ({ default: m.MenusCreatePage }))
);
const MenusDetailPage = lazy(() =>
  import('@/pages/quiz/menus/MenusDetailPage').then((m) => ({ default: m.MenusDetailPage }))
);
const MenusEditPage = lazy(() =>
  import('@/pages/quiz/menus/MenusEditPage').then((m) => ({ default: m.MenusEditPage }))
);

export const menusRoutes = createCrudRoutes('/menus', {
  List: MenusListPage,
  Create: MenusCreatePage,
  Detail: MenusDetailPage,
  Edit: MenusEditPage,
});
