import { HomePage } from '@/pages';
import type { RouteObject as AppRouteObject } from 'react-router-dom';

export const dashboardRoutes: AppRouteObject[] = [
  { path: '/', element: <HomePage /> },
  { path: '/dashboard', element: <HomePage /> },
];
