import { useState, useEffect, useRef } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Loader2, CheckCircle2, XCircle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { apiClient } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';
import { appTheme } from '@/theme';

type ActivationStatus = 'loading' | 'success' | 'error';

export function ActivatePage() {
  const { uid, token } = useParams<{ uid: string; token: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<ActivationStatus>('loading');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const hasAttemptedActivationRef = useRef(false);

  useEffect(() => {
    if (hasAttemptedActivationRef.current) {
      return;
    }
    hasAttemptedActivationRef.current = true;

    let redirectTimeout: ReturnType<typeof setTimeout> | null = null;

    const activateAccount = async () => {
      if (!uid || !token) {
        setStatus('error');
        setErrorMessage("Lien d'activation invalide.");
        return;
      }

      try {
        await apiClient.post(AUTH_ENDPOINTS.users.activation, { uid, token });
        setStatus('success');
        redirectTimeout = setTimeout(() => {
          navigate('/auth/login');
        }, 3000);
      } catch (err) {
        setStatus('error');
        if (err instanceof Error && 'response' in err) {
          const axiosError = err as { response?: { data?: { detail?: string } } };
          setErrorMessage(
            axiosError.response?.data?.detail || "Le lien d'activation est invalide ou a expiré."
          );
        } else {
          setErrorMessage("Une erreur est survenue lors de l'activation.");
        }
      }
    };

    activateAccount();

    return () => {
      if (redirectTimeout) {
        clearTimeout(redirectTimeout);
      }
    };
  }, [uid, token, navigate]);

  return (
    <AuthLayout>
      <div className="space-y-6 text-center">
        {status === 'loading' && (
          <>
            <Loader2 className="h-16 w-16 animate-spin text-denim mx-auto" />
            <div className="space-y-1">
              <h2
                className="text-2xl font-bold text-cream"
                style={{ fontFamily: "'Syne', system-ui" }}
              >
                Activation en cours...
              </h2>
              <p className="text-sm text-cream/50">Veuillez patienter</p>
            </div>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle2 className="h-16 w-16 text-lettuce mx-auto" />
            <div className="space-y-1">
              <h2
                className="text-2xl font-bold text-cream"
                style={{ fontFamily: "'Syne', system-ui" }}
              >
                Compte activé !
              </h2>
              <p className="text-sm text-cream/50">
                Redirection vers la connexion dans quelques secondes...
              </p>
            </div>
            <Button asChild size="lg" className="">
              <Link to="/auth/login">Se connecter maintenant</Link>
            </Button>
          </>
        )}

        {status === 'error' && (
          <>
            <XCircle className="h-16 w-16 text-ketchup mx-auto" />
            <div className="space-y-1">
              <h2
                className="text-2xl font-bold text-cream"
                style={{ fontFamily: "'Syne', system-ui" }}
              >
                Échec de l'activation
              </h2>
              <p className="text-sm text-cream/50">{errorMessage}</p>
            </div>
            <div className="flex flex-col gap-3">
              <Button asChild size="lg" className="">
                <Link to="/auth/resend-activation">Renvoyer le lien d'activation</Link>
              </Button>
              <Link to="/auth/login" className={appTheme.link.accent}>
                Retour à la connexion
              </Link>
            </div>
          </>
        )}
      </div>
    </AuthLayout>
  );
}
