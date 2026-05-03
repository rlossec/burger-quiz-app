import { lazy } from 'react';
import type { RouteObject } from 'react-router-dom';

const RoundsPage = lazy(() =>
  import('@/pages/quiz/RoundsPage').then((m) => ({ default: m.RoundsPage }))
);

export const roundsRoutes: RouteObject[] = [{ path: 'rounds', element: <RoundsPage /> }];
