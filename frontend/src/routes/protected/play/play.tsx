import {
  PlayHomePage,
  CreateSessionPage,
  JoinSessionPage,
  LobbyPage,
  GamePage,
  ResultsPage,
} from '@/pages';
import type { RouteObject as AppRouteObject } from 'react-router-dom';

export const playRoutes: AppRouteObject[] = [
  { path: '/play', element: <PlayHomePage /> },
  { path: '/play/create', element: <CreateSessionPage /> },
  { path: '/play/join', element: <JoinSessionPage /> },
  { path: '/play/:sessionId/lobby', element: <LobbyPage /> },
  { path: '/play/:sessionId/game', element: <GamePage /> },
  { path: '/play/:sessionId/results', element: <ResultsPage /> },
];
