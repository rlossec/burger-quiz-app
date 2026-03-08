import { Navigate } from 'react-router-dom';
import {
  ActivatePage,
  ResendActivationPage,
  ForgotPasswordPage,
  ResetPasswordPage,
  EmailSentPage,
} from '@/pages';
import { AuthLayout } from '@/components/layout';
import { LoginForm, RegisterForm } from '@/components/forms';
import { NotFoundPage } from '@/pages';

export const publicRoutes = [
  { path: '*', element: <NotFoundPage /> },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { index: true, element: <Navigate to="/auth/login" replace /> },
      { path: 'login', element: <LoginForm /> },
      { path: 'register', element: <RegisterForm /> },
    ],
  },
  { path: '/login', element: <Navigate to="/auth/login" replace /> },
  { path: '/register', element: <Navigate to="/auth/register" replace /> },
  { path: '/auth/activate/:uid/:token', element: <ActivatePage /> },
  { path: '/auth/resend-activation', element: <ResendActivationPage /> },
  { path: '/auth/forgot-password', element: <ForgotPasswordPage /> },
  { path: '/auth/password/reset/confirm/:uid/:token', element: <ResetPasswordPage /> },
  { path: '/auth/email-sent', element: <EmailSentPage /> },
];
