import type { ComponentType } from 'react';
import type { RouteObject as AppRouteObject } from 'react-router-dom';

interface CrudPages {
  List: ComponentType;
  Create: ComponentType;
  Detail: ComponentType;
  Edit: ComponentType;
}

export function createCrudRoutes(basePath: string, pages: CrudPages): AppRouteObject[] {
  const { List, Create, Detail, Edit } = pages;
  return [
    { path: basePath, element: <List /> },
    { path: `${basePath}/create`, element: <Create /> },
    { path: `${basePath}/:id`, element: <Detail /> },
    { path: `${basePath}/:id/edit`, element: <Edit /> },
  ];
}
