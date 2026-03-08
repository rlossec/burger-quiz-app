import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Link, useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

import { apiClient } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';
import { registerSchema, type RegisterFormData } from '@/features/auth/schemas/register';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

import { appTheme } from '@/theme';

export function RegisterForm() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post(AUTH_ENDPOINTS.users.register, data);
      navigate('/auth/email-sent', { state: { email: data.email, type: 'activation' } });
    } catch (error) {
      if (error instanceof Error && 'response' in error) {
        const axiosError = error as { response?: { data?: Record<string, string[]> } };
        const responseData = axiosError.response?.data;
        if (responseData) {
          const firstError = Object.values(responseData)[0];
          if (Array.isArray(firstError) && firstError.length > 0) {
            setError(firstError[0]);
          } else {
            setError('Une erreur est survenue. Veuillez réessayer.');
          }
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
        <h2 className="text-2xl font-bold text-cream" style={{ fontFamily: "'Syne', system-ui" }}>
          Créer un compte
        </h2>
        <p className="text-sm text-cream/50">Commencez votre aventure quiz</p>
      </div>

      {error && (
        <Alert variant="destructive" className="border-ketchup/30 bg-ketchup/10 text-cream">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-1.5">
          <Label htmlFor="username" className="text-sm font-medium text-cream/70">
            Identifiant
          </Label>
          <Input
            id="username"
            type="text"
            placeholder="votre_pseudo"
            autoComplete="username"
            aria-invalid={!!errors.username}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('username')}
          />
          {errors.username && <p className="text-xs text-ketchup">{errors.username.message}</p>}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="email" className="text-sm font-medium text-cream/70">
            Email
          </Label>
          <Input
            id="email"
            type="email"
            placeholder="votre@email.com"
            autoComplete="email"
            aria-invalid={!!errors.email}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('email')}
          />
          {errors.email && <p className="text-xs text-ketchup">{errors.email.message}</p>}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="password" className="text-sm font-medium text-cream/70">
            Mot de passe
          </Label>
          <Input
            id="password"
            type="password"
            autoComplete="new-password"
            aria-invalid={!!errors.password}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('password')}
          />
          {errors.password && <p className="text-xs text-ketchup">{errors.password.message}</p>}
        </div>

        <div className="space-y-1.5">
          <Label htmlFor="re_password" className="text-sm font-medium text-cream/70">
            Confirmer le mot de passe
          </Label>
          <Input
            id="re_password"
            type="password"
            autoComplete="new-password"
            aria-invalid={!!errors.re_password}
            className={`h-11 ${appTheme.input.dark}`}
            {...register('re_password')}
          />
          {errors.re_password && (
            <p className="text-xs text-ketchup">{errors.re_password.message}</p>
          )}
        </div>

        <Button type="submit" disabled={isLoading} size="lg" className="mt-2 w-full">
          {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
          S'inscrire
        </Button>
      </form>

      <p className="text-center text-sm text-cream/40">
        Déjà un compte ?{' '}
        <Link to="/auth/login" className={appTheme.link.accent}>
          Se connecter
        </Link>
      </p>
    </div>
  );
}
