import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

import { useAuthStore } from '@/stores';
import { apiClient, tokenStorage } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';
import { loginSchema, type LoginFormData } from '@/features/auth/schemas/login';
import type { AuthTokens, User } from '@/types/auth';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

import { appTheme } from '@/theme';

export function LoginForm() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const redirect = searchParams.get('redirect') || '/dashboard';
  const { login } = useAuthStore();

  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const tokenResponse = await apiClient.post<AuthTokens>(AUTH_ENDPOINTS.auth.login, data);
      const { access, refresh } = tokenResponse.data;
      tokenStorage.setTokens(access, refresh);
      const userResponse = await apiClient.get<User>(AUTH_ENDPOINTS.users.me);
      login(userResponse.data);
      navigate(redirect);
    } catch (err) {
      if (err instanceof Error && 'response' in err) {
        const axiosError = err as { response?: { status?: number; data?: { detail?: string } } };
        if (axiosError.response?.status === 401) {
          setError('Identifiant ou mot de passe incorrect');
        } else if (axiosError.response?.data?.detail) {
          setError(axiosError.response.data.detail);
        } else {
          setError('Une erreur est survenue. Veuillez réessayer.');
        }
      } else {
        setError('Une erreur est survenue. Veuillez réessayer.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h2
          className="text-2xl font-bold text-center text-cream"
          style={{ fontFamily: "'Syne', system-ui" }}
        >
          Connexion
        </h2>
      </div>

      {error && (
        <Alert variant="destructive" className="border-ketchup/30 bg-ketchup/10 text-cream">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="username" className="text-sm font-medium text-cream/70">
            Email ou identifiant
          </Label>
          <Input
            id="username"
            type="text"
            placeholder="votre@email.com"
            autoComplete="username"
            aria-invalid={!!errors.username}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('username')}
          />
          {errors.username && <p className="text-xs text-ketchup">{errors.username.message}</p>}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="password" className="text-sm font-medium text-cream/70">
            Mot de passe
          </Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            autoComplete="current-password"
            aria-invalid={!!errors.password}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('password')}
          />
          <div className="flex justify-end">
            <Link to="/auth/forgot-password" className={`text-xs ${appTheme.link.primary}`}>
              Mot de passe oublié ?
            </Link>
          </div>
          {errors.password && <p className="text-xs text-ketchup">{errors.password.message}</p>}
        </div>

        <Button type="submit" disabled={isLoading} size="lg" className="mt-2 w-full">
          {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
          Se connecter
        </Button>
      </form>

      <p className="text-center text-sm text-cream/40">
        Pas encore de compte ?{' '}
        <Link to="/auth/register" className={appTheme.link.accent}>
          S'inscrire
        </Link>
      </p>
    </div>
  );
}
