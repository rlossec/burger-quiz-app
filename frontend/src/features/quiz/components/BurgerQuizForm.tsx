import { Controller, useForm, type SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Loader2 } from 'lucide-react';

import { TagInput } from '@/components/common';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { burgerQuizFormSchema, type BurgerQuizFormData } from '@/features/quiz/schemas/burger-quiz';
import { useTagCatalog } from '@/features/quiz/hooks';
import { cn } from '@/lib/utils';

export interface BurgerQuizFormProps {
  defaultValues?: Partial<BurgerQuizFormData>;
  onSubmit: (data: BurgerQuizFormData) => void | Promise<void>;
  isLoading?: boolean;
  submitLabel?: string;
  cancelLabel?: string;
  onCancel?: () => void;
  /** Erreurs renvoyées par l'API (ex. 400) à afficher en priorité sur les champs */
  fieldErrors?: Record<string, string>;
  className?: string;
}

/**
 * Formulaire création/édition des infos de base d'un Burger Quiz (titre, toss, tags).
 */
export function BurgerQuizForm({
  defaultValues,
  onSubmit,
  isLoading = false,
  submitLabel = 'Enregistrer',
  cancelLabel = 'Annuler',
  onCancel,
  fieldErrors = {},
  className,
}: BurgerQuizFormProps) {
  const {
    control,
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<BurgerQuizFormData>({
    resolver: zodResolver(burgerQuizFormSchema),
    defaultValues: {
      title: '',
      toss: '',
      tags: [],
      ...defaultValues,
    },
  });
  const { data: tagCatalog = [], isError: tagCatalogError } = useTagCatalog();
  const submitHandler: SubmitHandler<BurgerQuizFormData> = (data) => onSubmit(data);

  const getError = (name: keyof BurgerQuizFormData) => fieldErrors[name] ?? errors[name]?.message;

  return (
    <form onSubmit={handleSubmit(submitHandler)} className={cn('space-y-5', className)} noValidate>
      <div className="space-y-2">
        <Label htmlFor="burger-quiz-title">
          Titre <span className="text-destructive">*</span>
        </Label>
        <Input
          id="burger-quiz-title"
          {...register('title')}
          placeholder="Titre du Burger Quiz"
          aria-invalid={!!getError('title')}
          disabled={isLoading}
          className="w-full"
        />
        {getError('title') && <p className="text-sm text-destructive">{getError('title')}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="burger-quiz-toss">
          Toss <span className="text-destructive">*</span>
        </Label>
        <Input
          id="burger-quiz-toss"
          {...register('toss')}
          placeholder="Phrase du toss"
          aria-invalid={!!getError('toss')}
          disabled={isLoading}
          className="w-full"
        />
        {getError('toss') && <p className="text-sm text-destructive">{getError('toss')}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="burger-quiz-tags">Tags</Label>
        <Controller
          control={control}
          name="tags"
          render={({ field }) => (
            <TagInput
              id="burger-quiz-tags"
              name={field.name}
              value={field.value ?? []}
              onChange={field.onChange}
              suggestions={tagCatalog}
              disabled={isLoading}
              ariaInvalid={!!getError('tags')}
              suggestionsUnavailableMessage={
                tagCatalogError
                  ? 'Suggestions indisponibles pour le moment. Vous pouvez saisir vos tags.'
                  : undefined
              }
            />
          )}
        />
        <p className="text-xs text-muted-foreground">
          Entrée ou virgule pour ajouter. Minimum 3 caractères, maximum 15 tags.
        </p>
        {getError('tags') && <p className="text-sm text-destructive">{getError('tags')}</p>}
      </div>

      <div className="flex flex-wrap items-center justify-end gap-2 pt-2">
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel} disabled={isLoading}>
            {cancelLabel}
          </Button>
        )}
        <Button type="submit" disabled={isLoading}>
          {isLoading && <Loader2 className="size-4 animate-spin" aria-hidden />}
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}
