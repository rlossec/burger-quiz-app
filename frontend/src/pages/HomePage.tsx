import { Link } from 'react-router-dom';
import { Play, PlusCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

export function HomePage() {
  const { cards, text, buttons, typography, spacing } = appTheme;

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
            L'expérience quiz ultime. Créez, jouez, gagnez.
          </p>
          <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:gap-4">
            <Button asChild size="lg" className={cn('w-full sm:w-auto', buttons.team.ketchup)}>
              <Link to="/play">
                <Play className="mr-2 h-5 w-5" />
                Jouer
              </Link>
            </Button>
            <Button asChild size="lg" className={cn('w-full sm:w-auto', buttons.team.mayo)}>
              <Link to="/quiz">
                <PlusCircle className="mr-2 h-5 w-5" />
                Créer un quiz
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
