import { Link, useLocation } from 'react-router-dom';
import { Mail } from 'lucide-react';

import { AuthLayout } from '@/components/layout/AuthLayout';

interface LocationState {
  email?: string;
  type?: 'activation' | 'password-reset';
}

export function EmailSentPage() {
  const location = useLocation();
  const state = location.state as LocationState | null;
  const email = state?.email;
  const type = state?.type || 'activation';

  const isActivation = type === 'activation';

  return (
    <AuthLayout>
      <div className="space-y-6 text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-denim/20">
          <Mail className="h-8 w-8 text-denim" />
        </div>

        <div className="space-y-1">
          <h2 className="text-2xl font-bold text-cream" style={{ fontFamily: "'Syne', system-ui" }}>
            {isActivation ? 'Vérifiez votre email' : 'Email envoyé'}
          </h2>
          <p className="text-sm text-cream/50">
            {isActivation
              ? "Un lien d'activation a été envoyé"
              : 'Un lien de réinitialisation a été envoyé'}
            {email && (
              <>
                {' à '}
                <span className="font-medium text-cream/70">{email}</span>
              </>
            )}
          </p>
        </div>

        <div className="rounded-lg bg-cream/5 p-4 text-sm text-cream/60">
          <p>
            {isActivation
              ? "Cliquez sur le lien dans l'email pour activer votre compte. Le lien expire dans 24 heures."
              : "Cliquez sur le lien dans l'email pour réinitialiser votre mot de passe. Le lien expire dans 1 heure."}
          </p>
        </div>

        <div className="space-y-3">
          {isActivation && (
            <Link
              to="/auth/resend-activation"
              className="block text-sm text-denim hover:text-denim/80 transition-colors"
            >
              Vous n'avez pas reçu l'email ? Renvoyer
            </Link>
          )}
          <Link
            to="/auth/login"
            className="block text-sm text-mustard hover:text-mustard/80 transition-colors"
          >
            Retour à la connexion
          </Link>
        </div>
      </div>
    </AuthLayout>
  );
}
