import { HomePage, DraftsPage } from '../pages';

export const commonRoutes = [
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/drafts',
    element: <DraftsPage />,
  },
];
