import { lazy } from 'react';
import { createCrudRoutes } from '@/routes/utils';

const SaltPepperListPage = lazy(() =>
  import('@/pages/quiz/salt-pepper/SaltPepperListPage').then((m) => ({
    default: m.SaltPepperListPage,
  }))
);
const SaltPepperCreatePage = lazy(() =>
  import('@/pages/quiz/salt-pepper/SaltPepperCreatePage').then((m) => ({
    default: m.SaltPepperCreatePage,
  }))
);
const SaltPepperDetailPage = lazy(() =>
  import('@/pages/quiz/salt-pepper/SaltPepperDetailPage').then((m) => ({
    default: m.SaltPepperDetailPage,
  }))
);
const SaltPepperEditPage = lazy(() =>
  import('@/pages/quiz/salt-pepper/SaltPepperEditPage').then((m) => ({
    default: m.SaltPepperEditPage,
  }))
);

export const saltPepperRoutes = createCrudRoutes('/salt-pepper', {
  List: SaltPepperListPage,
  Create: SaltPepperCreatePage,
  Detail: SaltPepperDetailPage,
  Edit: SaltPepperEditPage,
});
