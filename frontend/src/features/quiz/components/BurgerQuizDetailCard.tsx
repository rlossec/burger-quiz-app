import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Pencil } from 'lucide-react';
import type { BurgerQuizDetail } from '@/types';
import { appTheme } from '@/theme';
import { cn } from '@/lib/utils';

export interface BurgerQuizDetailCardProps {
  quiz: BurgerQuizDetail;
  onEdit: () => void;
  className?: string;
}

export function BurgerQuizDetailCard({ quiz, onEdit, className }: BurgerQuizDetailCardProps) {
  const { typography } = appTheme;
  const tagsLabel = quiz.tags?.length ? quiz.tags.join(' ') : '—';

  return (
    <Card className={cn('', className)}>
      <CardContent className="flex flex-col gap-4 pt-6 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-2 min-w-0">
          <div>
            <span className="text-sm font-medium text-muted-foreground">Titre : </span>
            <span className={typography.body}>{quiz.title}</span>
          </div>
          <div>
            <span className="text-sm font-medium text-muted-foreground">Toss : </span>
            <span className={typography.body}>{quiz.toss}</span>
          </div>
          <div>
            <span className="text-sm font-medium text-muted-foreground">Tags : </span>
            <span className={typography.body}>{tagsLabel}</span>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={onEdit} className="shrink-0">
          <Pencil className="size-4" aria-hidden />
          Modifier
        </Button>
      </CardContent>
    </Card>
  );
}
