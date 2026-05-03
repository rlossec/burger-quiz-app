import { Link } from 'react-router-dom';
import { Play, PlusCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

export function HomePage() {
  const { cards, text, typography, spacing } = appTheme;

  return (
    <div className={spacing.section.gap}>
      {/* Hero */}
      <section
        className={cn(
          'relative overflow-hidden rounded-3xl',
          spacing.section.padding,
          cards.hero,
          text.primary
        )}
      >
        <div className={cn('absolute inset-0', cards.heroOverlay)} />
        <div className="absolute right-4 top-4 text-6xl opacity-60 sm:right-8 sm:top-8 sm:text-8xl md:right-12 md:top-12">
          🍔
        </div>
        <div className="relative z-10 max-w-2xl space-y-4 sm:space-y-6">
          <h1 className={typography.h1}>
            <span className={text.accent.ketchup}>Burger</span>{' '}
            <span className={text.accent.mayo}>Quiz</span>
          </h1>
          <p className={cn(typography.bodyLarge, text.secondary)}>
            Gagnez des miams et remportez le Burger de la mort !
          </p>
          <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:gap-4">
            <Link
              to="/play"
              className="inline-flex h-11 w-full items-center justify-center gap-2 rounded-lg border-2 border-ketchup bg-transparent px-6 text-base font-semibold text-cream transition-colors hover:bg-ketchup/20 sm:w-auto"
            >
              <Play className="h-5 w-5" />
              Jouer
            </Link>
            <Link
              to="/quiz"
              className="inline-flex h-11 w-full items-center justify-center gap-2 rounded-lg border-2 border-mustard bg-transparent px-6 text-base font-semibold text-cream transition-colors hover:bg-mustard/20 sm:w-auto"
            >
              <PlusCircle className="h-5 w-5" />
              Créer un quiz
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
