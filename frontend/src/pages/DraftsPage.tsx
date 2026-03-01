import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

export function DraftsPage() {
  const { text, cards, buttons, typography, spacing } = appTheme;

  return (
    <div className={spacing.section.gap}>
      <h1 className={cn(typography.h2, text.primary)}>Design System - Drafts</h1>

      {/* Palette de couleurs */}
      <section className={cn('space-y-4 rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary)}>Palette de couleurs</h2>
        <div className="grid grid-cols-3 gap-3 sm:grid-cols-5 md:grid-cols-9">
          {[
            { name: 'Ketchup', bg: 'bg-ketchup' },
            { name: 'Mayo', bg: 'bg-mustard' },
            { name: 'Bun', bg: 'bg-bun' },
            { name: 'Lettuce', bg: 'bg-lettuce' },
            { name: 'Onion', bg: 'bg-onion' },
            { name: 'Denim', bg: 'bg-denim' },
            { name: 'Patty', bg: 'bg-patty' },
            { name: 'Dark', bg: 'bg-dark ring-1 ring-cream/20' },
            { name: 'Cream', bg: 'bg-cream' },
          ].map((color) => (
            <div key={color.name} className="space-y-1 text-center">
              <div className={cn('mx-auto h-10 w-10 rounded-lg sm:h-12 sm:w-12', color.bg)} />
              <p className={cn(typography.xs, text.muted)}>{color.name}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Boutons depuis appTheme */}
      <section className={cn('space-y-6 rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary)}>Boutons (via appTheme)</h2>

        <div className="space-y-2">
          <p className={cn(typography.small, text.muted)}>Primary & Secondary</p>
          <div className="flex flex-wrap gap-2 sm:gap-3">
            <Button className={buttons.primary}>Primary (Denim)</Button>
            <Button className={buttons.secondary}>Secondary (Onion)</Button>
          </div>
        </div>

        <div className="space-y-2">
          <p className={cn(typography.small, text.muted)}>Outline</p>
          <div className="flex flex-wrap gap-2 sm:gap-3">
            <Button className={buttons.outline.ketchup}>Ketchup</Button>
            <Button className={buttons.outline.mayo}>Mayo</Button>
            <Button className={buttons.outline.denim}>Denim</Button>
            <Button className={buttons.outline.onion}>Onion</Button>
            <Button className={buttons.outline.lettuce}>Lettuce</Button>
          </div>
        </div>

        <div className="space-y-2">
          <p className={cn(typography.small, text.muted)}>Ghost</p>
          <div className="flex flex-wrap gap-2 sm:gap-3">
            <Button className={buttons.ghost.bun}>Ghost Bun</Button>
            <Button className={buttons.ghost.denim}>Ghost Denim</Button>
          </div>
        </div>

        <div className="space-y-2">
          <p className={cn(typography.small, text.muted)}>Équipes</p>
          <div className="flex flex-wrap gap-2 sm:gap-3">
            <Button className={buttons.team.ketchup}>🍅 Équipe Ketchup</Button>
            <Button className={buttons.team.mayo}>🥚 Équipe Mayo</Button>
          </div>
        </div>
      </section>

      {/* Typography */}
      <section className={cn('space-y-4 rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary)}>Typography (via appTheme.typography)</h2>
        <div className="space-y-3">
          <p className={cn(typography.h1, text.primary)}>h1 - Titre principal</p>
          <p className={cn(typography.h2, text.primary)}>h2 - Titre secondaire</p>
          <p className={cn(typography.h3, text.primary)}>h3 - Sous-titre</p>
          <p className={cn(typography.h4, text.primary)}>h4 - Petit titre</p>
          <p className={cn(typography.bodyLarge, text.secondary)}>bodyLarge - Corps large</p>
          <p className={cn(typography.body, text.secondary)}>body - Corps standard</p>
          <p className={cn(typography.small, text.muted)}>small - Petit texte</p>
          <p className={cn(typography.xs, text.muted)}>xs - Très petit</p>
        </div>
      </section>

      {/* Textes couleurs */}
      <section className={cn('space-y-4 rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary)}>Couleurs de texte (via appTheme.text)</h2>
        <div className="space-y-2">
          <p className={text.primary}>text.primary - Texte principal</p>
          <p className={text.secondary}>text.secondary - Texte secondaire</p>
          <p className={text.muted}>text.muted - Texte atténué</p>
          <p className={text.inactive}>text.inactive - Texte inactif</p>
          <p className={text.subtle}>text.subtle - Texte subtil</p>
        </div>
        <div className="flex flex-wrap gap-3 sm:gap-4">
          <span className={text.accent.ketchup}>accent.ketchup</span>
          <span className={text.accent.mayo}>accent.mayo</span>
          <span className={text.accent.bun}>accent.bun</span>
          <span className={text.accent.denim}>accent.denim</span>
          <span className={text.accent.onion}>accent.onion</span>
          <span className={text.accent.lettuce}>accent.lettuce</span>
        </div>
      </section>
    </div>
  );
}
