import { ProfilePage } from '@/pages';
import type { RouteObject as AppRouteObject } from 'react-router-dom';

export const profileRoutes: AppRouteObject[] = [{ path: '/profile', element: <ProfilePage /> }];
