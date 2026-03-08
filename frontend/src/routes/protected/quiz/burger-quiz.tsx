import { lazy } from 'react';
import type { RouteObject } from 'react-router-dom';

const BurgerQuizListPage = lazy(() =>
  import('@/pages/quiz/BurgerQuizListPage').then((m) => ({ default: m.BurgerQuizListPage }))
);
const BurgerQuizCreatePage = lazy(() =>
  import('@/pages/quiz/BurgerQuizCreatePage').then((m) => ({ default: m.BurgerQuizCreatePage }))
);
const BurgerQuizDetailEdit = lazy(() =>
  import('@/pages/quiz/BurgerQuizDetailEdit').then((m) => ({ default: m.BurgerQuizDetailEdit }))
);

export const burgerQuizRoutes: RouteObject[] = [
  { path: 'quiz', element: <BurgerQuizListPage /> },
  { path: 'quiz/create', element: <BurgerQuizCreatePage /> },
  { path: 'quiz/:id', element: <BurgerQuizDetailEdit /> },
];
