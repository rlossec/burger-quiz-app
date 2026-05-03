import { cn } from '@/lib/utils';
import { appTheme, colors } from '@/theme';

const mainColors = [
  { name: 'Ketchup', css: 'ketchup', hex: '#B73229', desc: 'Équipe rouge, erreurs' },
  { name: 'Mustard', css: 'mustard', hex: '#F7C438', desc: 'Équipe jaune, accents' },
  { name: 'Denim', css: 'denim', hex: '#6B7DB3', desc: 'Primary, liens, actions' },
  { name: 'Bun', css: 'bun', hex: '#E59752', desc: 'Logo, badges, warmth' },
  { name: 'Lettuce', css: 'lettuce', hex: '#5B8C3E', desc: 'Succès, validation' },
  { name: 'Onion', css: 'onion', hex: '#8B4A6B', desc: 'Secondary, navigation active' },
  { name: 'Patty', css: 'patty', hex: '#5C3D2E', desc: 'Header, footer, surfaces' },
  { name: 'Dark', css: 'dark', hex: '#0E0C0B', desc: 'Background principal' },
  { name: 'Cream', css: 'cream', hex: '#F2EBE1', desc: 'Texte sur fond sombre' },
];

const opacities = [10, 20, 30, 50, 70, 90];

export function ColorsPage() {
  const { text, cards, typography, spacing } = appTheme;

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      <div className="space-y-2">
        <h1 className={cn(typography.h2, text.primary)}>Palette de couleurs</h1>
        <p className={cn(typography.body, text.muted)}>
          Toutes les couleurs sont définies en OKLCH pour un meilleur contrôle perceptuel.
        </p>
      </div>

      {/* Couleurs principales */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Couleurs principales</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {mainColors.map((color) => (
            <div key={color.name} className="flex items-center gap-4 rounded-xl bg-cream/5 p-4">
              <div className={cn('h-14 w-14 rounded-xl shadow-lg', `bg-${color.css}`)} />
              <div className="flex-1 min-w-0">
                <p className={cn(typography.h4, text.primary)}>{color.name}</p>
                <p className={cn(typography.xs, text.muted, 'font-mono')}>{color.hex}</p>
                <p className={cn(typography.xs, text.subtle)}>{color.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Opacités */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Opacités</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Utilisation : <code className="bg-cream/10 px-1.5 py-0.5 rounded">bg-color/opacity</code>
        </p>

        <div className="space-y-4">
          {['ketchup', 'denim', 'mustard', 'cream'].map((colorName) => (
            <div key={colorName} className="space-y-2">
              <p className={cn(typography.small, text.secondary, 'capitalize')}>{colorName}</p>
              <div className="flex gap-2">
                {opacities.map((op) => (
                  <div key={op} className="text-center">
                    <div className={cn('h-10 w-10 rounded-lg', `bg-${colorName}/${op}`)} />
                    <span className={cn(typography.xs, text.muted)}>/{op}</span>
                  </div>
                ))}
                <div className="text-center">
                  <div className={cn('h-10 w-10 rounded-lg', `bg-${colorName}`)} />
                  <span className={cn(typography.xs, text.muted)}>100</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Valeurs OKLCH */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-2')}>Valeurs OKLCH (theme/colors.ts)</h2>
        <p className={cn(typography.small, text.muted, 'mb-6')}>
          Pour les styles inline, importer depuis <code className="bg-cream/10 px-1.5 py-0.5 rounded">@/theme</code>
        </p>

        <div className="grid gap-2 font-mono text-sm">
          {Object.entries(colors).map(([key, value]) => {
            if (typeof value === 'string') {
              return (
                <div key={key} className="flex items-center gap-4 rounded bg-cream/5 px-3 py-2">
                  <div
                    className="h-6 w-6 rounded"
                    style={{ background: value }}
                  />
                  <span className={text.secondary}>{key}:</span>
                  <span className={text.muted}>{value}</span>
                </div>
              );
            }
            return null;
          })}
        </div>
      </section>

      {/* Usage */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-4')}>Usage</h2>
        <div className="space-y-4 font-mono text-sm">
          <div className="rounded bg-cream/5 p-4">
            <p className={text.muted}>// Tailwind (via CSS variables)</p>
            <p className={text.primary}>className="bg-ketchup text-cream"</p>
          </div>
          <div className="rounded bg-cream/5 p-4">
            <p className={text.muted}>// Inline styles (valeurs brutes)</p>
            <p className={text.primary}>{`style={{ background: colors.ketchup }}`}</p>
          </div>
          <div className="rounded bg-cream/5 p-4">
            <p className={text.muted}>// appTheme (classes composées)</p>
            <p className={text.primary}>{`className={appTheme.text.accent.ketchup}`}</p>
          </div>
        </div>
      </section>
    </div>
  );
}
