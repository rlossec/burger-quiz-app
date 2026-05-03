import { useState } from 'react';
import { Eye, EyeOff, Check, AlertCircle, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

export function FormsPage() {
  const { text, cards, typography, spacing, input, link } = appTheme;
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      <div className="space-y-2">
        <h1 className={cn(typography.h2, text.primary)}>Formulaires</h1>
        <p className={cn(typography.body, text.muted)}>
          Inputs, labels, validations et feedback utilisateur.
        </p>
      </div>

      {/* Inputs de base */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Inputs de base</h2>

        <div className="grid gap-6 sm:grid-cols-2">
          <div className="space-y-2">
            <Label className="text-cream/70">Input standard (fond clair)</Label>
            <Input placeholder="Entrez du texte..." />
          </div>

          <div className="space-y-2">
            <Label className="text-cream/70">Input fond sombre (appTheme.input.dark)</Label>
            <Input placeholder="Entrez du texte..." className={input.dark} />
          </div>
        </div>
      </section>

      {/* Types d'inputs */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Types d'inputs</h2>

        <div className="grid gap-6 sm:grid-cols-2">
          <div className="space-y-2">
            <Label className="text-cream/70">Email</Label>
            <Input type="email" placeholder="votre@email.com" className={input.dark} />
          </div>

          <div className="space-y-2">
            <Label className="text-cream/70">Mot de passe</Label>
            <div className="relative">
              <Input
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                className={cn(input.dark, 'pr-10')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-cream/50 hover:text-cream"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <div className="space-y-2">
            <Label className="text-cream/70">Nombre</Label>
            <Input type="number" placeholder="42" className={input.dark} />
          </div>

          <div className="space-y-2">
            <Label className="text-cream/70">Recherche</Label>
            <Input type="search" placeholder="Rechercher..." className={input.dark} />
          </div>
        </div>
      </section>

      {/* États de validation */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>États de validation</h2>

        <div className="grid gap-6 sm:grid-cols-2">
          {/* Succès */}
          <div className="space-y-2">
            <Label className="text-cream/70">Valide</Label>
            <Input
              value="utilisateur_valide"
              readOnly
              className={cn(input.dark, 'border-lettuce/50 focus-visible:ring-lettuce/50')}
            />
            <p className="flex items-center gap-1.5 text-sm text-lettuce">
              <Check className="h-4 w-4" /> Nom d'utilisateur disponible
            </p>
          </div>

          {/* Erreur */}
          <div className="space-y-2">
            <Label className="text-cream/70">Erreur</Label>
            <Input
              value="a"
              readOnly
              aria-invalid
              className={cn(input.dark, 'border-ketchup/50 focus-visible:ring-ketchup/50')}
            />
            <p className="flex items-center gap-1.5 text-sm text-ketchup">
              <AlertCircle className="h-4 w-4" /> Minimum 3 caractères requis
            </p>
          </div>

          {/* Info */}
          <div className="space-y-2">
            <Label className="text-cream/70">Avec info</Label>
            <Input placeholder="votre@email.com" className={input.dark} />
            <p className="flex items-center gap-1.5 text-sm text-denim">
              <Info className="h-4 w-4" /> Un email de confirmation sera envoyé
            </p>
          </div>

          {/* Disabled */}
          <div className="space-y-2">
            <Label className="text-cream/70">Désactivé</Label>
            <Input value="Non modifiable" disabled className={input.dark} />
          </div>
        </div>
      </section>

      {/* Liens */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Liens (appTheme.link)</h2>

        <div className="space-y-4">
          <p>
            <a href="#" className={link.primary}>
              link.primary
            </a>
          </p>
          <p>
            <a href="#" className={link.accent}>
              link.accent
            </a>
          </p>
          <p>
            <a href="#" className={link.muted}>
              link.muted
            </a>
          </p>
        </div>
      </section>

      {/* Formulaire exemple */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Formulaire exemple</h2>

        <form className="max-w-md space-y-4">
          <div className="space-y-2">
            <Label htmlFor="demo-email" className="text-cream/70">
              Email <span className="text-ketchup">*</span>
            </Label>
            <Input
              id="demo-email"
              type="email"
              placeholder="votre@email.com"
              className={input.dark}
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="demo-password" className="text-cream/70">
                Mot de passe <span className="text-ketchup">*</span>
              </Label>
              <a href="#" className={cn('text-xs', link.primary)}>
                Mot de passe oublié ?
              </a>
            </div>
            <Input
              id="demo-password"
              type="password"
              placeholder="••••••••"
              className={input.dark}
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="demo-remember"
              className="h-4 w-4 rounded border-cream/20 bg-cream/5"
            />
            <Label htmlFor="demo-remember" className="text-sm text-cream/70">
              Se souvenir de moi
            </Label>
          </div>

          <Button type="button" size="lg" className="w-full">
            Se connecter
          </Button>

          <p className="text-center text-sm text-cream/50">
            Pas encore de compte ?{' '}
            <a href="#" className={link.accent}>
              S'inscrire
            </a>
          </p>
        </form>
      </section>

      {/* Alert boxes */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Alertes & messages</h2>

        <div className="space-y-4">
          <div className="flex items-start gap-3 rounded-lg bg-lettuce/10 p-4 ring-1 ring-lettuce/30">
            <Check className="h-5 w-5 shrink-0 text-lettuce" />
            <div>
              <p className="font-medium text-lettuce">Succès</p>
              <p className={cn(typography.small, text.muted)}>Votre profil a été mis à jour.</p>
            </div>
          </div>

          <div className="flex items-start gap-3 rounded-lg bg-ketchup/10 p-4 ring-1 ring-ketchup/30">
            <AlertCircle className="h-5 w-5 shrink-0 text-ketchup" />
            <div>
              <p className="font-medium text-ketchup">Erreur</p>
              <p className={cn(typography.small, text.muted)}>
                Une erreur est survenue. Réessayez.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 rounded-lg bg-mustard/10 p-4 ring-1 ring-mustard/30">
            <AlertCircle className="h-5 w-5 shrink-0 text-mustard" />
            <div>
              <p className="font-medium text-mustard">Attention</p>
              <p className={cn(typography.small, text.muted)}>Cette action est irréversible.</p>
            </div>
          </div>

          <div className="flex items-start gap-3 rounded-lg bg-denim/10 p-4 ring-1 ring-denim/30">
            <Info className="h-5 w-5 shrink-0 text-denim" />
            <div>
              <p className="font-medium text-denim">Information</p>
              <p className={cn(typography.small, text.muted)}>
                Votre session expire dans 5 minutes.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
