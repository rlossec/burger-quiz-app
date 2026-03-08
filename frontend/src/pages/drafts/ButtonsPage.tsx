import { Play, Plus, Trash2, Settings, LogOut, User, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

export function ButtonsPage() {
  const { text, cards, typography, spacing, buttons } = appTheme;

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      <div className="space-y-2">
        <h1 className={cn(typography.h2, text.primary)}>Boutons</h1>
        <p className={cn(typography.body, text.muted)}>
          Composant Button de Shadcn avec variants personnalisés du thème.
        </p>
      </div>

      {/* Variants Shadcn */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Variants Shadcn (par défaut)</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Primary = Denim (via --primary CSS variable)
        </p>

        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <Button>Default (Primary)</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </div>
        </div>
      </section>

      {/* Tailles */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Tailles</h2>

        <div className="flex flex-wrap items-center gap-3">
          <Button size="xs">Extra Small</Button>
          <Button size="sm">Small</Button>
          <Button size="default">Default</Button>
          <Button size="lg">Large</Button>
          <Button size="icon"><Settings className="h-4 w-4" /></Button>
          <Button size="icon-sm"><Settings className="h-4 w-4" /></Button>
          <Button size="icon-lg"><Settings className="h-5 w-5" /></Button>
        </div>
      </section>

      {/* Avec icônes */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Avec icônes</h2>

        <div className="flex flex-wrap items-center gap-3">
          <Button><Play className="h-4 w-4" /> Jouer</Button>
          <Button variant="secondary"><Plus className="h-4 w-4" /> Créer</Button>
          <Button variant="destructive"><Trash2 className="h-4 w-4" /> Supprimer</Button>
          <Button variant="outline"><Settings className="h-4 w-4" /> Paramètres</Button>
        </div>
      </section>

      {/* États */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>États</h2>

        <div className="flex flex-wrap items-center gap-3">
          <Button>Normal</Button>
          <Button disabled>Disabled</Button>
          <Button className="pointer-events-none opacity-70">
            <span className="animate-spin mr-2">⏳</span> Loading...
          </Button>
        </div>
      </section>

      {/* Boutons thème personnalisés */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Boutons thème (appTheme.buttons)</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Cas spéciaux définis dans le thème.
        </p>

        <div className="space-y-6">
          {/* Outline colorés */}
          <div className="space-y-2">
            <p className={cn(typography.small, text.secondary)}>Outline colorés</p>
            <div className="flex flex-wrap items-center gap-3">
              <Button className={buttons.outline.ketchup}>
                <Play className="h-4 w-4" /> Ketchup
              </Button>
              <Button className={buttons.outline.mustard}>
                <Plus className="h-4 w-4" /> Mustard
              </Button>
            </div>
          </div>

          {/* Équipes */}
          <div className="space-y-2">
            <p className={cn(typography.small, text.secondary)}>Équipes</p>
            <div className="flex flex-wrap items-center gap-3">
              <Button className={buttons.team.ketchup}>
                🍅 Équipe Ketchup
              </Button>
              <Button className={buttons.team.mayo}>
                🥚 Équipe Mayo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Header buttons */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Boutons Header (appTheme.headerButtons)</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Styles spécifiques pour le header de l'application.
        </p>

        <div className="flex flex-wrap items-center gap-3 rounded-xl bg-patty/50 p-4">
          <button className={cn('rounded-lg p-2 transition-colors', appTheme.headerButtons.profile)}>
            <User className="h-5 w-5" />
          </button>
          <button className={cn('rounded-lg p-2 transition-colors', appTheme.headerButtons.logout)}>
            <LogOut className="h-5 w-5" />
          </button>
          <button className={cn('rounded-lg p-2 transition-colors', appTheme.headerButtons.menu)}>
            <Settings className="h-5 w-5" />
          </button>
        </div>
      </section>

      {/* Composition exemple */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.hero)}>
        <div className={cn('absolute inset-0', cards.heroOverlay)} />
        <div className="relative space-y-4">
          <h3 className={cn(typography.h3, text.primary)}>Prêt à jouer ?</h3>
          <p className={cn(typography.body, text.secondary)}>
            Rejoignez une partie ou créez votre propre quiz.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button size="lg" className={buttons.outline.ketchup}>
              <Play className="h-5 w-5" /> Rejoindre
            </Button>
            <Button size="lg" className={buttons.outline.mustard}>
              <Plus className="h-5 w-5" /> Créer un quiz
            </Button>
          </div>
        </div>
      </section>

      {/* Boutons d'action */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Boutons d'action contextuels</h2>

        <div className="space-y-4">
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div>
              <p className={text.primary}>Supprimer ce quiz ?</p>
              <p className={cn(typography.small, text.muted)}>Cette action est irréversible.</p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm">
                <X className="h-4 w-4" /> Annuler
              </Button>
              <Button variant="destructive" size="sm">
                <Trash2 className="h-4 w-4" /> Supprimer
              </Button>
            </div>
          </div>

          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div>
              <p className={text.primary}>Sauvegarder les modifications ?</p>
              <p className={cn(typography.small, text.muted)}>3 changements non enregistrés.</p>
            </div>
            <div className="flex gap-2">
              <Button variant="ghost" size="sm">Annuler</Button>
              <Button size="sm">
                <Check className="h-4 w-4" /> Enregistrer
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
