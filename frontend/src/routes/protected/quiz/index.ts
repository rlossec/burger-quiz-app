import { burgerQuizRoutes } from './burger-quiz';
import { additionRoutes } from './addition';
import { deadlyBurgerRoutes } from './deadly-burger';
import { menusRoutes } from './menus';
import { nuggetsRoutes } from './nuggets';
import { saltPepperRoutes } from './salt-pepper';
import { interludesRoutes } from './interludes';
import { roundsRoutes } from './rounds';

export const quizRoutes = [
  ...roundsRoutes,
  ...saltPepperRoutes,
  ...nuggetsRoutes,
  ...menusRoutes,
  ...additionRoutes,
  ...deadlyBurgerRoutes,
  ...burgerQuizRoutes,
  ...interludesRoutes,
];
