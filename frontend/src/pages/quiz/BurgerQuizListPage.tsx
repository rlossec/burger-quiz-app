import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Pencil, Trash2, Search, CheckCircle2, PencilLine, CircleOff } from 'lucide-react';

import { ConfirmDialog } from '@/components/common';
import { PageWrapper } from '@/components/layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { appTheme } from '@/theme';
import { getApiErrorMessage } from '@/lib/api-error';
import type { BurgerQuizDetail, BurgerQuizListParams } from '@/types';
import { useBurgerQuizListQuery, useDeleteBurgerQuizMutation } from '@/features/quiz/hooks';
import { cn } from '@/lib/utils';
import { getRoundVisual, type RoundSlug } from '@/features/quiz/constants/roundVisuals';

type RoundStatus = 'complete' | 'missing' | 'partial';
type QuizRoundSlug = 'nuggets' | 'salt_or_pepper' | 'menus' | 'addition' | 'deadly_burger';

function getRoundStatus(quiz: BurgerQuizDetail, roundSlug: QuizRoundSlug): RoundStatus {
  const hasRound = quiz.structure?.some((el) => el.type === roundSlug);
  return hasRound ? 'complete' : 'missing';
}

interface RoundStatusPillProps {
  status: RoundStatus;
  label: string;
}

const ROUND_STATUS_STYLES = {
  missing: 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-300',
  partial: 'bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200',
  complete: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200',
} as const;

function RoundStatusPill({ status, label }: RoundStatusPillProps) {
  const Icon = status === 'complete' ? CheckCircle2 : status === 'partial' ? PencilLine : CircleOff;
  const ariaLabel =
    status === 'complete'
      ? `${label} complète`
      : status === 'partial'
        ? `${label} partielle`
        : `${label} absente`;

  return (
    <span
      className={cn(
        'inline-flex size-7 items-center justify-center rounded-full text-sm',
        ROUND_STATUS_STYLES[status]
      )}
      title={ariaLabel}
      aria-label={ariaLabel}
    >
      <Icon className="size-4" aria-hidden />
    </span>
  );
}

interface RoundHeaderProps {
  slug: RoundSlug;
}

function RoundHeader({ slug }: RoundHeaderProps) {
  const { label, icon: Icon, iconClassName, iconBgClassName } = getRoundVisual(slug);

  return (
    <span
      className="inline-flex items-center justify-center gap-1.5"
      title={label}
      aria-label={label}
    >
      <span
        className={cn('flex size-6 items-center justify-center rounded-md', iconBgClassName)}
        aria-hidden
      >
        <Icon className={cn('size-3.5', iconClassName)} />
      </span>
    </span>
  );
}

interface BurgerQuizRowProps {
  quiz: BurgerQuizDetail;
  onEdit: () => void;
  onDelete: () => void;
}

function BurgerQuizRow({ quiz, onEdit, onDelete }: BurgerQuizRowProps) {
  const date = new Date(quiz.created_at);
  const formattedDate = date.toLocaleDateString();

  return (
    <tr className="border-b last:border-b-0 transition-colors hover:bg-muted/30">
      <td className="px-4 py-2 text-sm font-medium text-foreground">{quiz.title}</td>
      <td className="px-4 py-2 text-sm text-muted-foreground whitespace-nowrap">{formattedDate}</td>
      <td className="px-2 py-2 text-center">
        <RoundStatusPill status={getRoundStatus(quiz, 'nuggets')} label="Nuggets" />
      </td>
      <td className="px-2 py-2 text-center">
        <RoundStatusPill status={getRoundStatus(quiz, 'salt_or_pepper')} label="Sel ou Poivre" />
      </td>
      <td className="px-2 py-2 text-center">
        <RoundStatusPill status={getRoundStatus(quiz, 'menus')} label="Menus" />
      </td>
      <td className="px-2 py-2 text-center">
        <RoundStatusPill status={getRoundStatus(quiz, 'addition')} label="Addition" />
      </td>
      <td className="px-2 py-2 text-center">
        <RoundStatusPill status={getRoundStatus(quiz, 'deadly_burger')} label="Burger de la mort" />
      </td>
      <td className="px-4 py-2">
        <div className="flex items-center justify-end gap-1">
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onEdit}
            title="Modifier"
            aria-label="Modifier le quiz"
          >
            <Pencil className="size-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon-sm"
            className="text-destructive hover:bg-destructive/10 hover:text-destructive"
            onClick={onDelete}
            title="Supprimer"
            aria-label="Supprimer le quiz"
          >
            <Trash2 className="size-4" />
          </Button>
        </div>
      </td>
    </tr>
  );
}

interface BurgerQuizTableProps {
  quizzes: BurgerQuizDetail[];
  onEdit: (quiz: BurgerQuizDetail) => void;
  onDelete: (quiz: BurgerQuizDetail) => void;
}

function BurgerQuizTable({ quizzes, onEdit, onDelete }: BurgerQuizTableProps) {
  const { typography } = appTheme;

  if (quizzes.length === 0) {
    return (
      <div className="py-6 text-sm text-muted-foreground">
        Aucun Burger Quiz pour le moment. Cliquez sur « Créer » pour commencer.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full table-fixed border-separate border-spacing-0">
        <thead>
          <tr className="border-b">
            <th className="px-4 py-2 text-left text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Titre
            </th>
            <th className="px-4 py-2 text-left text-xs font-semibold uppercase tracking-wide text-muted-foreground whitespace-nowrap">
              Date
            </th>
            <th className="px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <RoundHeader slug="nuggets" />
            </th>
            <th className="px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <RoundHeader slug="salt_or_pepper" />
            </th>
            <th className="px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <RoundHeader slug="menus" />
            </th>
            <th className="px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <RoundHeader slug="addition" />
            </th>
            <th className="px-2 py-2 text-center text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              <RoundHeader slug="deadly_burger" />
            </th>
            <th className="px-4 py-2 text-right text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className={typography.body}>
          {quizzes.map((quiz) => (
            <BurgerQuizRow
              key={quiz.id}
              quiz={quiz}
              onEdit={() => onEdit(quiz)}
              onDelete={() => onDelete(quiz)}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

const ORDERING_OPTIONS: { value: string; label: string }[] = [
  { value: '-created_at', label: 'Plus récents' },
  { value: 'created_at', label: 'Plus anciens' },
  { value: 'title', label: 'Titre A–Z' },
  { value: '-title', label: 'Titre Z–A' },
  { value: '-updated_at', label: 'Modifiés récemment' },
];

interface BurgerQuizListFiltersProps {
  search: string;
  ordering: string;
  onSearchChange: (value: string) => void;
  onOrderingChange: (value: string) => void;
}

function BurgerQuizListFilters({
  search,
  ordering,
  onSearchChange,
  onOrderingChange,
}: BurgerQuizListFiltersProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
      <div className="relative flex-1 min-w-0">
        <Search
          className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
          aria-hidden
        />
        <Input
          type="search"
          placeholder="Rechercher par titre…"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="pl-9"
          aria-label="Rechercher un Burger Quiz"
        />
      </div>
      <div className="flex items-center gap-2 sm:shrink-0">
        <label
          htmlFor="quiz-ordering"
          className="text-sm font-medium text-muted-foreground whitespace-nowrap"
        >
          Trier par
        </label>
        <select
          id="quiz-ordering"
          value={ordering}
          onChange={(e) => onOrderingChange(e.target.value)}
          className={cn(
            'h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-xs',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
            'disabled:pointer-events-none disabled:opacity-50'
          )}
          aria-label="Ordre d'affichage"
        >
          {ORDERING_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

const DEFAULT_ORDERING = '-created_at';
const SEARCH_DEBOUNCE_MS = 300;

function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(t);
  }, [value, delayMs]);
  return debounced;
}

export function BurgerQuizListPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [ordering, setOrdering] = useState(DEFAULT_ORDERING);
  const debouncedSearch = useDebouncedValue(search, SEARCH_DEBOUNCE_MS);

  const listParams = useMemo<BurgerQuizListParams>(() => {
    const params: BurgerQuizListParams = { ordering };
    if (debouncedSearch.trim()) params.search = debouncedSearch.trim();
    return params;
  }, [debouncedSearch, ordering]);

  const { data, isLoading, isError, error } = useBurgerQuizListQuery(listParams);
  const deleteMutation = useDeleteBurgerQuizMutation();
  const [quizToDelete, setQuizToDelete] = useState<BurgerQuizDetail | null>(null);

  const quizzes = data?.results ?? [];

  const handleCreate = () => {
    navigate('create');
  };

  const handleEdit = (quiz: BurgerQuizDetail) => {
    navigate(quiz.id);
  };

  const handleDeleteConfirm = async () => {
    if (!quizToDelete) return;
    await deleteMutation.mutateAsync(quizToDelete.id);
  };

  const { typography } = appTheme;

  return (
    <PageWrapper className="py-6 md:py-10">
      <ConfirmDialog
        open={!!quizToDelete}
        onOpenChange={(open) => !open && setQuizToDelete(null)}
        title="Supprimer le Burger Quiz"
        description={
          quizToDelete ? `« ${quizToDelete.title} » sera supprimé définitivement. Continuer ?` : ''
        }
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        variant="destructive"
        onConfirm={handleDeleteConfirm}
        isLoading={deleteMutation.isPending}
      />
      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4 border-b">
          <div>
            <CardTitle className={typography.h2}>Burger Quiz</CardTitle>
          </div>
          <Button onClick={handleCreate}>+ Créer</Button>
        </CardHeader>
        <CardContent className="space-y-4">
          <BurgerQuizListFilters
            search={search}
            ordering={ordering}
            onSearchChange={setSearch}
            onOrderingChange={setOrdering}
          />
          {isLoading && (
            <div className="py-6 text-sm text-muted-foreground">Chargement des quizzes…</div>
          )}
          {isError && (
            <div className="py-6 text-sm text-destructive">
              {getApiErrorMessage(error) || 'Impossible de charger la liste des Burger Quiz.'}
            </div>
          )}
          {!isLoading && !isError && (
            <BurgerQuizTable
              quizzes={quizzes}
              onEdit={handleEdit}
              onDelete={(quiz) => setQuizToDelete(quiz)}
            />
          )}
        </CardContent>
      </Card>
    </PageWrapper>
  );
}
