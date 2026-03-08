import {
  DraftsIndexPage,
  ColorsPage,
  TypographyPage,
  ButtonsPage,
  CardsPage,
  FormsPage,
} from '@/pages';
import type { RouteObject as AppRouteObject } from 'react-router-dom';

/** Routes temporaires Design System - Drafts. */
export const draftsRoutes: AppRouteObject[] = [
  { path: '/drafts', element: <DraftsIndexPage /> },
  { path: '/drafts/colors', element: <ColorsPage /> },
  { path: '/drafts/typography', element: <TypographyPage /> },
  { path: '/drafts/buttons', element: <ButtonsPage /> },
  { path: '/drafts/cards', element: <CardsPage /> },
  { path: '/drafts/forms', element: <FormsPage /> },
];
