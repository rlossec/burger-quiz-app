import { Link } from 'react-router-dom';
import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';

import { PageWrapper } from '@/components/layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { appTheme } from '@/theme';
import { getApiErrorMessage } from '@/lib/api-error';
import { cn } from '@/lib/utils';
import type { BurgerQuizDetail, StructureElementSlug } from '@/types';
import {
  useAdditionListQuery,
  useBurgerQuizListQuery,
  useDeadlyBurgerListQuery,
  useMenusListQuery,
  useNuggetsListQuery,
  useSaltPepperListQuery,
} from '@/features/quiz/hooks';
import { interludesApi, queryKeys } from '@/features/quiz/api';
import {
  getRoundVisual,
  type RoundSlug,
  VIDEO_INTERLUDE_VISUAL,
} from '@/features/quiz/constants/roundVisuals';

type ManagedRoundSlug = RoundSlug | 'video_interlude';

interface RoundHubCard {
  slug: ManagedRoundSlug;
  route: string;
}

const ROUND_CARDS: RoundHubCard[] = [
  { slug: 'nuggets', route: '/nuggets' },
  { slug: 'salt_or_pepper', route: '/salt-pepper' },
  { slug: 'menus', route: '/menus' },
  { slug: 'addition', route: '/addition' },
  { slug: 'deadly_burger', route: '/deadly-burger' },
  { slug: 'video_interlude', route: '/interludes' },
];

function buildUsedMap(quizzes: BurgerQuizDetail[]): Record<ManagedRoundSlug, number> {
  const perType: Record<ManagedRoundSlug, Set<string>> = {
    nuggets: new Set(),
    salt_or_pepper: new Set(),
    menus: new Set(),
    addition: new Set(),
    deadly_burger: new Set(),
    video_interlude: new Set(),
  };

  quizzes.forEach((quiz) => {
    quiz.structure.forEach((el) => {
      const type = el.type as StructureElementSlug;
      if (
        type === 'nuggets' ||
        type === 'salt_or_pepper' ||
        type === 'menus' ||
        type === 'addition' ||
        type === 'deadly_burger' ||
        type === 'video_interlude'
      ) {
        perType[type].add(el.id);
      }
    });
  });

  return {
    nuggets: perType.nuggets.size,
    salt_or_pepper: perType.salt_or_pepper.size,
    menus: perType.menus.size,
    addition: perType.addition.size,
    deadly_burger: perType.deadly_burger.size,
    video_interlude: perType.video_interlude.size,
  };
}

function getManagedVisual(slug: ManagedRoundSlug) {
  if (slug === 'video_interlude') return VIDEO_INTERLUDE_VISUAL;
  return getRoundVisual(slug);
}

export function RoundsPage() {
  const { typography } = appTheme;

  const listParams = { page_size: 100 };
  const burgerQuizListQuery = useBurgerQuizListQuery(listParams);
  const nuggetsListQuery = useNuggetsListQuery(listParams);
  const saltPepperListQuery = useSaltPepperListQuery(listParams);
  const menusListQuery = useMenusListQuery(listParams);
  const additionListQuery = useAdditionListQuery(listParams);
  const deadlyBurgerListQuery = useDeadlyBurgerListQuery(listParams);
  const interludesListQuery = useQuery({
    queryKey: [...queryKeys.interludes.lists(), listParams],
    queryFn: () => interludesApi.list(listParams),
  });

  const isLoading =
    burgerQuizListQuery.isLoading ||
    nuggetsListQuery.isLoading ||
    saltPepperListQuery.isLoading ||
    menusListQuery.isLoading ||
    additionListQuery.isLoading ||
    deadlyBurgerListQuery.isLoading ||
    interludesListQuery.isLoading;

  const globalError =
    burgerQuizListQuery.error ||
    nuggetsListQuery.error ||
    saltPepperListQuery.error ||
    menusListQuery.error ||
    additionListQuery.error ||
    deadlyBurgerListQuery.error ||
    interludesListQuery.error;

  const usedByType = useMemo(
    () => buildUsedMap(burgerQuizListQuery.data?.results ?? []),
    [burgerQuizListQuery.data?.results]
  );

  const createdByType: Record<ManagedRoundSlug, number> = {
    nuggets: nuggetsListQuery.data?.count ?? 0,
    salt_or_pepper: saltPepperListQuery.data?.count ?? 0,
    menus: menusListQuery.data?.count ?? 0,
    addition: additionListQuery.data?.count ?? 0,
    deadly_burger: deadlyBurgerListQuery.data?.count ?? 0,
    video_interlude: interludesListQuery.data?.count ?? 0,
  };

  return (
    <PageWrapper className="space-y-6 py-6 md:py-10">
      <Card>
        <CardHeader className="border-b">
          <CardTitle className={typography.h2}>Manches</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          {isLoading ? (
            <p className="text-sm text-muted-foreground">Chargement des statistiques…</p>
          ) : globalError ? (
            <p className="text-sm text-destructive">
              {getApiErrorMessage(globalError) ??
                'Impossible de charger les statistiques des manches.'}
            </p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {ROUND_CARDS.map((card) => {
                const created = createdByType[card.slug];
                const used = usedByType[card.slug] ?? 0;
                const unused = Math.max(0, created - used);
                const {
                  label,
                  icon: Icon,
                  iconBgClassName,
                  iconClassName,
                } = getManagedVisual(card.slug);

                return (
                  <Card key={card.slug}>
                    <CardHeader className="pb-2">
                      <CardTitle className="flex items-center gap-2 text-lg">
                        <span
                          className={cn(
                            'flex size-8 items-center justify-center rounded-md',
                            iconBgClassName
                          )}
                          aria-hidden
                        >
                          <Icon className={cn('size-4', iconClassName)} />
                        </span>
                        {label}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-1">
                      <p className="text-sm">
                        Créées : <span className="font-semibold">{created}</span>
                      </p>
                      <p className="text-sm">
                        Utilisées : <span className="font-semibold">{used}</span>
                      </p>
                      <p className="text-sm">
                        Non utilisées : <span className="font-semibold">{unused}</span>
                      </p>
                      <Button asChild variant="outline" size="sm" className="mt-3 w-full">
                        <Link to={card.route}>Voir la liste</Link>
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </PageWrapper>
  );
}
