import { Play, Clock, Users, Trophy, Star, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

export function CardsPage() {
  const { text, cards, typography, spacing } = appTheme;

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      <div className="space-y-2">
        <h1 className={cn(typography.h2, text.primary)}>Cards & Conteneurs</h1>
        <p className={cn(typography.body, text.muted)}>
          Styles de cartes et mises en page pour différents contextes.
        </p>
      </div>

      {/* Cards de base */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Cards de base (appTheme.cards)</h2>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
            <h3 className={cn(typography.h4, text.primary)}>cards.default</h3>
            <p className={cn(typography.small, text.muted, 'mt-2')}>
              bg-dark/50 ring-1 ring-cream/10
            </p>
          </div>

          <div className={cn('relative rounded-2xl overflow-hidden', spacing.card.padding, cards.hero)}>
            <div className={cn('absolute inset-0', cards.heroOverlay)} />
            <div className="relative">
              <h3 className={cn(typography.h4, text.primary)}>cards.hero</h3>
              <p className={cn(typography.small, text.muted, 'mt-2')}>
                bg-dark/80 + heroOverlay gradient
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Quiz cards */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Cards de quiz</h2>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { title: 'Culture Générale', questions: 42, plays: 156, color: 'denim' },
            { title: 'Sport & Loisirs', questions: 38, plays: 89, color: 'ketchup' },
            { title: 'Cinéma & Séries', questions: 55, plays: 234, color: 'mustard' },
          ].map((quiz) => (
            <div
              key={quiz.title}
              className={cn(
                'group relative rounded-2xl transition-all hover:scale-[1.02]',
                spacing.card.padding,
                cards.default
              )}
            >
              <div className={cn('absolute inset-x-0 top-0 h-1 rounded-t-2xl', `bg-${quiz.color}`)} />
              <div className="space-y-3">
                <h3 className={cn(typography.h4, text.primary, 'group-hover:text-mustard transition-colors')}>
                  {quiz.title}
                </h3>
                <div className="flex items-center gap-4 text-sm">
                  <span className={text.muted}>
                    <Clock className="inline h-4 w-4 mr-1" />
                    {quiz.questions} questions
                  </span>
                  <span className={text.muted}>
                    <Users className="inline h-4 w-4 mr-1" />
                    {quiz.plays} parties
                  </span>
                </div>
                <Button size="sm" variant="ghost" className="w-full justify-between">
                  Voir le quiz <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Stat cards */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Stat cards</h2>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: 'Parties jouées', value: '1,234', icon: Play, color: 'ketchup' },
            { label: 'Questions créées', value: '567', icon: Star, color: 'mustard' },
            { label: 'Joueurs actifs', value: '89', icon: Users, color: 'denim' },
            { label: 'Victoires', value: '42', icon: Trophy, color: 'lettuce' },
          ].map((stat) => (
            <div
              key={stat.label}
              className="flex items-center gap-4 rounded-xl bg-cream/5 p-4"
            >
              <div className={cn('rounded-xl p-3', `bg-${stat.color}/20`)}>
                <stat.icon className={cn('h-6 w-6', `text-${stat.color}`)} />
              </div>
              <div>
                <p className={cn(typography.h3, text.primary)}>{stat.value}</p>
                <p className={cn(typography.xs, text.muted)}>{stat.label}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Équipes cards */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h3, text.primary, 'mb-6')}>Cards d'équipes</h2>

        <div className="grid gap-4 sm:grid-cols-2">
          {/* Équipe Ketchup */}
          <div className="relative overflow-hidden rounded-2xl bg-ketchup/10 p-6 ring-2 ring-ketchup/30">
            <div className="absolute -right-4 -top-4 text-8xl opacity-20">🍅</div>
            <div className="relative space-y-4">
              <div className="flex items-center gap-3">
                <span className="text-4xl">🍅</span>
                <div>
                  <h3 className={cn(typography.h3, 'text-ketchup')}>Équipe Ketchup</h3>
                  <p className={cn(typography.small, text.muted)}>3 joueurs</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={cn(typography.h2, 'text-ketchup')}>12</span>
                <span className={text.muted}>miams</span>
              </div>
            </div>
          </div>

          {/* Équipe Mayo */}
          <div className="relative overflow-hidden rounded-2xl bg-mustard/10 p-6 ring-2 ring-mustard/30">
            <div className="absolute -right-4 -top-4 text-8xl opacity-20">🥚</div>
            <div className="relative space-y-4">
              <div className="flex items-center gap-3">
                <span className="text-4xl">🥚</span>
                <div>
                  <h3 className={cn(typography.h3, 'text-mustard')}>Équipe Mayo</h3>
                  <p className={cn(typography.small, text.muted)}>3 joueurs</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={cn(typography.h2, 'text-mustard')}>9</span>
                <span className={text.muted}>miams</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Hero card */}
      <section className={cn('relative overflow-hidden rounded-3xl', spacing.section.padding, cards.hero)}>
        <div className={cn('absolute inset-0', cards.heroOverlay)} />
        <div className="absolute right-4 top-4 text-6xl opacity-60 sm:right-8 sm:top-8 sm:text-8xl">
          🍔
        </div>
        <div className="relative z-10 max-w-2xl space-y-4">
          <h2 className={cn(typography.h1, text.primary)}>
            <span className={text.accent.ketchup}>Burger</span>{' '}
            <span className={text.accent.mayo}>Quiz</span>
          </h2>
          <p className={cn(typography.bodyLarge, text.secondary)}>
            Gagnez des miams et remportez le Burger de la mort !
          </p>
          <div className="flex flex-wrap gap-3">
            <Button size="lg" className={appTheme.buttons.outline.ketchup}>
              <Play className="h-5 w-5" /> Jouer
            </Button>
            <Button size="lg" className={appTheme.buttons.outline.mustard}>
              Créer un quiz
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
