import { Link } from 'react-router-dom';
import { Palette, Type, MousePointerClick, LayoutGrid, FormInput } from 'lucide-react';
import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

const draftPages = [
  {
    title: 'Couleurs',
    description: 'Palette complète et variantes de transparence',
    icon: Palette,
    href: '/drafts/colors',
    color: 'bg-ketchup/20 text-ketchup',
  },
  {
    title: 'Typographie',
    description: 'Tailles, poids et styles de texte',
    icon: Type,
    href: '/drafts/typography',
    color: 'bg-denim/20 text-denim',
  },
  {
    title: 'Boutons',
    description: 'Variants, tailles et états',
    icon: MousePointerClick,
    href: '/drafts/buttons',
    color: 'bg-mustard/20 text-mustard',
  },
  {
    title: 'Cards',
    description: 'Conteneurs et mises en page',
    icon: LayoutGrid,
    href: '/drafts/cards',
    color: 'bg-onion/20 text-onion',
  },
  {
    title: 'Formulaires',
    description: 'Inputs, labels et validations',
    icon: FormInput,
    href: '/drafts/forms',
    color: 'bg-lettuce/20 text-lettuce',
  },
];

export function DraftsIndexPage() {
  const { text, cards, typography, spacing } = appTheme;

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      {/* Header */}
      <div className="space-y-2">
        <h1 className={cn(typography.h1, text.primary)}>
          <span className="text-ketchup">Design</span> <span className="text-mustard">System</span>
        </h1>
        <p className={cn(typography.bodyLarge, text.muted)}>
          Explorez les composants et styles du thème Burger Quiz
        </p>
      </div>

      {/* Navigation cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {draftPages.map((page) => (
          <Link
            key={page.href}
            to={page.href}
            className={cn(
              'group relative overflow-hidden rounded-2xl p-6 transition-all hover:scale-[1.02]',
              cards.default
            )}
          >
            <div className="flex items-start gap-4">
              <div className={cn('rounded-xl p-3', page.color)}>
                <page.icon className="h-6 w-6" />
              </div>
              <div className="flex-1">
                <h3 className={cn(typography.h4, text.primary, 'group-hover:text-mustard transition-colors')}>
                  {page.title}
                </h3>
                <p className={cn(typography.small, text.muted)}>{page.description}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick preview */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-4')}>Aperçu rapide</h2>
        
        <div className="grid gap-4 sm:grid-cols-2">
          {/* Palette mini */}
          <div className="space-y-2">
            <p className={cn(typography.small, text.muted)}>Palette</p>
            <div className="flex gap-2">
              {['bg-ketchup', 'bg-mustard', 'bg-denim', 'bg-bun', 'bg-lettuce', 'bg-onion', 'bg-patty'].map((bg) => (
                <div key={bg} className={cn('h-8 w-8 rounded-lg', bg)} />
              ))}
            </div>
          </div>

          {/* Textes mini */}
          <div className="space-y-2">
            <p className={cn(typography.small, text.muted)}>Textes</p>
            <div className="flex flex-wrap gap-x-4 gap-y-1">
              <span className={text.primary}>Primary</span>
              <span className={text.secondary}>Secondary</span>
              <span className={text.muted}>Muted</span>
              <span className={text.accent.ketchup}>Accent</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
