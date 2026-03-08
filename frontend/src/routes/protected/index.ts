import { dashboardRoutes } from './dashboard';
import { draftsRoutes } from './drafts';
import { profileRoutes } from './profile';
import { playRoutes } from './play/play';
import { quizRoutes } from './quiz';

export const protectedRoutes = [
  ...dashboardRoutes,
  ...draftsRoutes,
  ...profileRoutes,
  ...playRoutes,
  ...quizRoutes,
];
