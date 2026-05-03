import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Loader2, CheckCircle2, XCircle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { apiClient } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';
import { appTheme } from '@/theme';

const resetPasswordSchema = z
  .object({
    new_password: z
      .string()
      .min(8, 'Le mot de passe doit contenir au moins 8 caractères')
      .regex(/[A-Z]/, 'Le mot de passe doit contenir au moins une majuscule')
      .regex(/[a-z]/, 'Le mot de passe doit contenir au moins une minuscule')
      .regex(/[0-9]/, 'Le mot de passe doit contenir au moins un chiffre'),
    re_new_password: z.string(),
  })
  .refine((data) => data.new_password === data.re_new_password, {
    message: 'Les mots de passe ne correspondent pas',
    path: ['re_new_password'],
  });

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>;
type ResetStatus = 'form' | 'success' | 'error';

export function ResetPasswordPage() {
  const { uid, token } = useParams<{ uid: string; token: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<ResetStatus>('form');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (!uid || !token) {
      setStatus('error');
      setError('Lien de réinitialisation invalide.');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post(AUTH_ENDPOINTS.users.resetPasswordConfirm, {
        uid,
        token,
        new_password: data.new_password,
        re_new_password: data.re_new_password,
      });
      setStatus('success');
      setTimeout(() => {
        navigate('/auth/login');
      }, 3000);
    } catch (err) {
      if (err instanceof Error && 'response' in err) {
        const axiosError = err as { response?: { data?: { detail?: string; token?: string[] } } };
        if (axiosError.response?.data?.token) {
          setStatus('error');
          setError('Le lien de réinitialisation est invalide ou a expiré.');
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

  if (status === 'success') {
    return (
      <AuthLayout>
        <div className="space-y-6 text-center">
          <CheckCircle2 className="h-16 w-16 text-lettuce mx-auto" />
          <div className="space-y-1">
            <h2
              className="text-2xl font-bold text-cream"
              style={{ fontFamily: "'Syne', system-ui" }}
            >
              Mot de passe modifié !
            </h2>
            <p className="text-sm text-cream/50">
              Redirection vers la connexion dans quelques secondes...
            </p>
          </div>
          <Button asChild size="lg" className="">
            <Link to="/auth/login">Se connecter maintenant</Link>
          </Button>
        </div>
      </AuthLayout>
    );
  }

  if (status === 'error' && !error) {
    return (
      <AuthLayout>
        <div className="space-y-6 text-center">
          <XCircle className="h-16 w-16 text-ketchup mx-auto" />
          <div className="space-y-1">
            <h2
              className="text-2xl font-bold text-cream"
              style={{ fontFamily: "'Syne', system-ui" }}
            >
              Lien expiré
            </h2>
            <p className="text-sm text-cream/50">
              Le lien de réinitialisation est invalide ou a expiré.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Button asChild size="lg" className="">
              <Link to="/auth/forgot-password">Demander un nouveau lien</Link>
            </Button>
            <Link to="/auth/login" className={appTheme.link.accent}>
              Retour à la connexion
            </Link>
          </div>
        </div>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout>
      <div className="space-y-6">
        <div className="space-y-1">
          <h2 className="text-2xl font-bold text-cream" style={{ fontFamily: "'Syne', system-ui" }}>
            Nouveau mot de passe
          </h2>
          <p className="text-sm text-cream/50">Choisissez un mot de passe sécurisé</p>
        </div>

        {error && (
          <Alert variant="destructive" className="border-ketchup/30 bg-ketchup/10 text-cream">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="new_password" className="text-sm font-medium text-cream/70">
              Nouveau mot de passe
            </Label>
            <Input
              id="new_password"
              type="password"
              autoComplete="new-password"
              aria-invalid={!!errors.new_password}
              className={`h-11 ${appTheme.input.dark}`}
              {...register('new_password')}
            />
            {errors.new_password && (
              <p className="text-xs text-ketchup">{errors.new_password.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="re_new_password" className="text-sm font-medium text-cream/70">
              Confirmer le mot de passe
            </Label>
            <Input
              id="re_new_password"
              type="password"
              autoComplete="new-password"
              aria-invalid={!!errors.re_new_password}
              className={`h-11 ${appTheme.input.dark}`}
              {...register('re_new_password')}
            />
            {errors.re_new_password && (
              <p className="text-xs text-ketchup">{errors.re_new_password.message}</p>
            )}
          </div>

          <Button type="submit" disabled={isLoading} size="lg" className="w-full mt-2">
            {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
            Réinitialiser le mot de passe
          </Button>
        </form>

        <p className="text-center text-sm text-cream/40">
          <Link to="/login" className={appTheme.link.accent}>
            Retour à la connexion
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
