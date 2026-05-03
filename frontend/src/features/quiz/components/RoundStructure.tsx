import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Plus, Link2, Pencil, Unlink } from 'lucide-react';
import type { BurgerQuizDetail } from '@/types';
import { appTheme } from '@/theme';
import { cn } from '@/lib/utils';
import { ROUND_SLUGS, getRoundVisual } from '@/features/quiz/constants/roundVisuals';
import { getRoundTitle } from '@/features/quiz/utils/structure';

export interface RoundStructureProps {
  quiz: BurgerQuizDetail;
  onUpdate?: () => void;
}

/**
 * Conteneur des 5 types de manches avec actions Créer / Attacher / Éditer / Détacher.
 * Les modales (création, recherche) sont à brancher ultérieurement.
 */
export function RoundStructure({ quiz }: RoundStructureProps) {
  const { typography } = appTheme;

  return (
    <Card>
      <CardHeader className="border-b">
        <CardTitle className={typography.h3}>Structure des manches</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 pt-6">
        {ROUND_SLUGS.map((slug) => {
          const { label, icon: Icon, iconClassName, iconBgClassName } = getRoundVisual(slug);
          const title = getRoundTitle(quiz, slug);
          const isEmpty = !title;

          return (
            <div
              key={slug}
              className="flex flex-wrap items-center justify-between gap-2 rounded-lg border bg-muted/20 px-4 py-3"
            >
              <div className="flex items-center gap-3 min-w-0">
                <span
                  className={cn(
                    'flex size-8 items-center justify-center rounded-md',
                    iconBgClassName
                  )}
                  aria-hidden
                >
                  <Icon className={cn('size-4', iconClassName)} />
                </span>
                <div className="min-w-0">
                  <span className="text-sm font-medium text-foreground">{label}</span>
                  <p
                    className={cn(
                      'text-sm truncate',
                      title ? 'text-muted-foreground' : 'text-muted-foreground italic'
                    )}
                  >
                    {title ?? 'Aucune manche'}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                {isEmpty ? (
                  <>
                    <Button variant="outline" size="sm" disabled title="Créer (bientôt)">
                      <Plus className="size-4" aria-hidden />
                      Créer
                    </Button>
                    <Button variant="outline" size="sm" disabled title="Attacher (bientôt)">
                      <Link2 className="size-4" aria-hidden />
                      Attacher
                    </Button>
                  </>
                ) : (
                  <>
                    <Button variant="ghost" size="icon-sm" disabled title="Éditer (bientôt)">
                      <Pencil className="size-4" aria-hidden />
                    </Button>
                    <Button variant="ghost" size="icon-sm" disabled title="Changer (bientôt)">
                      <Link2 className="size-4" aria-hidden />
                    </Button>
                    <Button variant="ghost" size="icon-sm" disabled title="Détacher (bientôt)">
                      <Unlink className="size-4" aria-hidden />
                    </Button>
                  </>
                )}
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
