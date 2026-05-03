import { useState, useMemo, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Trash2, Plus, ChevronUp, ChevronDown } from 'lucide-react';
import type { BurgerQuizStructureElement, BurgerQuizStructureElementWrite } from '@/types';
import { appTheme } from '@/theme';
import { cn } from '@/lib/utils';
import { ROUND_VISUALS, VIDEO_INTERLUDE_VISUAL } from '@/features/quiz/constants/roundVisuals';

function elementLabel(el: BurgerQuizStructureElement): string {
  if (el.type === 'video_interlude') {
    return el.video_interlude?.title ?? VIDEO_INTERLUDE_VISUAL.label;
  }
  return ROUND_VISUALS[el.type].label;
}

function elementVisual(el: BurgerQuizStructureElement) {
  if (el.type === 'video_interlude') return VIDEO_INTERLUDE_VISUAL;
  return ROUND_VISUALS[el.type];
}

function elementToWrite(el: BurgerQuizStructureElement): BurgerQuizStructureElementWrite {
  return { type: el.type, id: el.id };
}

export interface QuizStructureEditorProps {
  structure: BurgerQuizStructureElement[];
  onSave: (elements: BurgerQuizStructureElementWrite[]) => void | Promise<void>;
  isLoading?: boolean;
  hasCustomStructure?: boolean;
}

/**
 * Éditeur de la structure ordonnée (manches + interludes) avec réorganisation et sauvegarde.
 */
export function QuizStructureEditor({
  structure,
  onSave,
  isLoading = false,
  hasCustomStructure = true,
}: QuizStructureEditorProps) {
  const { typography } = appTheme;
  const [elements, setElements] = useState<BurgerQuizStructureElement[]>(structure);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setElements(structure);
  }, [structure]);

  const ordered = useMemo(() => [...elements].sort((a, b) => a.order - b.order), [elements]);

  const move = (index: number, direction: 'up' | 'down') => {
    const next = [...ordered];
    const target = direction === 'up' ? index - 1 : index + 1;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    setElements(next.map((el, i) => ({ ...el, order: i + 1 })));
  };

  const remove = (index: number) => {
    const el = ordered[index];
    if (el?.type !== 'video_interlude') return;
    const next = ordered.filter((_, i) => i !== index).map((e, i) => ({ ...e, order: i + 1 }));
    setElements(next);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const payload = ordered.map(elementToWrite);
      await Promise.resolve(onSave(payload));
    } finally {
      setIsSaving(false);
    }
  };

  const canRemove = (el: BurgerQuizStructureElement) => el.type === 'video_interlude';

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between gap-4 border-b">
        <div className="flex items-center gap-2">
          <CardTitle className={typography.h3}>Structure ordonnée</CardTitle>
          {!hasCustomStructure && (
            <span
              className="inline-flex items-center justify-center rounded-full bg-amber-100 px-2 py-0.5 text-xs font-medium text-amber-900 dark:bg-amber-900/40 dark:text-amber-100"
              title="Aucune structure enregistrée : affichage aligné sur le détail du quiz."
            >
              !
            </span>
          )}
        </div>
        <Button variant="outline" size="sm" disabled title="Ajouter un interlude (bientôt)">
          <Plus className="size-4" />
          Interlude
        </Button>
      </CardHeader>
      <CardContent className="pt-6 space-y-2">
        {ordered.length === 0 ? (
          <p className="text-sm text-muted-foreground py-4">
            Aucun élément. Ajoutez des manches à la structure du quiz puis enregistrez.
          </p>
        ) : (
          <ul className="space-y-1" role="list">
            {ordered.map((el, index) => {
              const label = elementLabel(el);
              const { icon: Icon, iconClassName, iconBgClassName } = elementVisual(el);

              return (
                <li
                  key={`${el.type}-${el.order}-${el.id}-${index}`}
                  className="flex items-center gap-2 rounded-lg border bg-muted/20 px-3 py-2"
                >
                  <div className="flex items-center gap-1 shrink-0">
                    <span className="text-xs font-medium text-muted-foreground w-6">
                      {index + 1}.
                    </span>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon-xs"
                      onClick={() => move(index, 'up')}
                      disabled={index === 0}
                      aria-label="Monter"
                    >
                      <ChevronUp className="size-4" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon-xs"
                      onClick={() => move(index, 'down')}
                      disabled={index === ordered.length - 1}
                      aria-label="Descendre"
                    >
                      <ChevronDown className="size-4" />
                    </Button>
                  </div>
                  <span
                    className={cn(
                      'flex size-8 shrink-0 items-center justify-center rounded-md',
                      iconBgClassName
                    )}
                    aria-hidden
                  >
                    <Icon className={cn('size-4', iconClassName)} />
                  </span>
                  <span className="text-sm font-medium truncate flex-1 min-w-0">{label}</span>
                  {canRemove(el) ? (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon-sm"
                      onClick={() => remove(index)}
                      className="text-destructive hover:bg-destructive/10"
                      aria-label="Supprimer"
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  ) : (
                    <span className="w-9" aria-hidden />
                  )}
                </li>
              );
            })}
          </ul>
        )}
        <p className="text-xs text-muted-foreground pt-2">
          Réorganisez avec les flèches. Les manches sont obligatoires, les interludes peuvent être
          supprimés.
        </p>
        <Button
          onClick={handleSave}
          disabled={isLoading || isSaving || ordered.length === 0}
          className="mt-4"
        >
          {isSaving ? 'Enregistrement…' : 'Enregistrer la structure'}
        </Button>
      </CardContent>
    </Card>
  );
}
