import { Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Layout } from '@/components/layout';
import { ProtectedRoute, publicRoutes, protectedRoutes } from '@/routes';
import { PageLoader } from '@/components/common';

const router = createBrowserRouter([
  // Routes publiques
  ...publicRoutes,

  // Routes protégées
  {
    element: <Layout />,
    children: [
      {
        element: <ProtectedRoute />,
        children: protectedRoutes,
      },
    ],
  },
]);

export default function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
