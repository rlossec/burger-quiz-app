import { cn } from '@/lib/utils';
import { appTheme, fonts } from '@/theme';

export function TypographyPage() {
  const { text, cards, typography, spacing } = appTheme;

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      <div className="space-y-2">
        <h1 className={cn(typography.h2, text.primary)}>Typographie</h1>
        <p className={cn(typography.body, text.muted)}>
          Échelle typographique responsive et styles de texte.
        </p>
      </div>

      {/* Polices */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Polices (theme/fonts.ts)</h2>
        <div className="space-y-6">
          <div className="space-y-2">
            <p className={cn(typography.small, text.muted)}>Heading - Syne</p>
            <p
              className={cn('text-4xl font-bold', text.primary)}
              style={{ fontFamily: fonts.heading }}
            >
              Burger Quiz 🍔
            </p>
          </div>
          <div className="space-y-2">
            <p className={cn(typography.small, text.muted)}>Body - DM Sans</p>
            <p className={cn('text-lg', text.secondary)} style={{ fontFamily: fonts.body }}>
              Le quiz où tout le monde peut devenir le roi du burger ! Gagnez des miams et affrontez
              vos amis dans des manches épiques.
            </p>
          </div>
        </div>
      </section>

      {/* Échelle typographique */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Échelle (appTheme.typography)</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Toutes les tailles sont responsive avec des breakpoints sm/md/lg.
        </p>

        <div className="space-y-6">
          {[
            { key: 'h1', label: 'H1', desc: 'text-3xl → 6xl, font-black' },
            { key: 'h2', label: 'H2', desc: 'text-2xl → 4xl, font-bold' },
            { key: 'h3', label: 'H3', desc: 'text-xl → 2xl, font-bold' },
            { key: 'h4', label: 'H4', desc: 'text-lg → xl, font-semibold' },
            { key: 'bodyLarge', label: 'Body Large', desc: 'text-lg → xl' },
            { key: 'body', label: 'Body', desc: 'text-base' },
            { key: 'small', label: 'Small', desc: 'text-sm' },
            { key: 'xs', label: 'XS', desc: 'text-xs' },
          ].map((item) => (
            <div
              key={item.key}
              className="flex items-baseline gap-4 border-b border-cream/10 pb-4 last:border-0"
            >
              <div className="w-24 shrink-0">
                <span className={cn(typography.xs, 'font-mono text-denim')}>{item.key}</span>
              </div>
              <div className="flex-1">
                <p className={cn(typography[item.key as keyof typeof typography], text.primary)}>
                  {item.label} - Burger Quiz
                </p>
                <p className={cn(typography.xs, text.muted, 'mt-1')}>{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Couleurs de texte */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>
          Couleurs de texte (appTheme.text)
        </h2>

        <div className="grid gap-6 sm:grid-cols-2">
          {/* Neutres */}
          <div className="space-y-3">
            <p className={cn(typography.small, text.muted, 'uppercase tracking-wide')}>Neutres</p>
            <div className="space-y-2">
              {[
                { key: 'primary', label: 'Texte principal' },
                { key: 'secondary', label: 'Texte secondaire' },
                { key: 'muted', label: 'Texte atténué' },
                { key: 'inactive', label: 'Texte inactif' },
                { key: 'subtle', label: 'Texte subtil' },
              ].map((item) => (
                <p key={item.key} className={text[item.key as keyof typeof text] as string}>
                  {item.key} - {item.label}
                </p>
              ))}
            </div>
          </div>

          {/* Accents */}
          <div className="space-y-3">
            <p className={cn(typography.small, text.muted, 'uppercase tracking-wide')}>Accents</p>
            <div className="space-y-2">
              {Object.entries(text.accent).map(([key, className]) => (
                <p key={key} className={className}>
                  accent.{key}
                </p>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Exemple de composition */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.hero)}>
        <div className={cn('absolute inset-0', cards.heroOverlay)} />
        <div className="relative space-y-4">
          <h2 className={cn(typography.h1, text.primary)}>
            <span className={text.accent.ketchup}>Burger</span>{' '}
            <span className={text.accent.mayo}>Quiz</span>
          </h2>
          <p className={cn(typography.bodyLarge, text.secondary)}>
            Créez et animez vos propres émissions quiz en vocal sur Discord.
          </p>
          <p className={cn(typography.small, text.muted)}>
            Plus de 1000 questions disponibles • Manches variées • Classements en direct
          </p>
        </div>
      </section>
    </div>
  );
}
