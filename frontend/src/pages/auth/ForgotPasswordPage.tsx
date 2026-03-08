import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { apiClient } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';
import { appTheme } from '@/theme';

const forgotPasswordSchema = z.object({
  email: z.email('Adresse email invalide'),
});

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>;

export function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  });

  const onSubmit = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post(AUTH_ENDPOINTS.users.resetPassword, { email: data.email });
      navigate('/auth/email-sent', { state: { email: data.email, type: 'password-reset' } });
    } catch {
      navigate('/auth/email-sent', { state: { email: data.email, type: 'password-reset' } });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout>
      <div className="space-y-6">
        <div className="space-y-1">
          <h2 className="text-2xl font-bold text-cream" style={{ fontFamily: "'Syne', system-ui" }}>
            Mot de passe oublié
          </h2>
          <p className="text-sm text-cream/50">
            Entrez votre email pour recevoir un lien de réinitialisation
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="border-ketchup/30 bg-ketchup/10 text-cream">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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

          <Button type="submit" disabled={isLoading} size="lg" className="w-full mt-2">
            {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
            Envoyer le lien
          </Button>
        </form>

        <p className="text-center text-sm text-cream/40">
          <Link to="/auth/login" className={appTheme.link.accent}>
            Retour à la connexion
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
}
