import { useState, useMemo } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Trash2 } from 'lucide-react';

import { ConfirmDialog } from '@/components/common';
import { PageWrapper } from '@/components/layout';
import { Button } from '@/components/ui/button';
import { appTheme } from '@/theme';
import { getApiErrorMessage, getApiFieldErrors } from '@/lib/api-error';
import type { BurgerQuizFormData } from '@/features/quiz/schemas/burger-quiz';
import type { BurgerQuizStructureElement, BurgerQuizStructureElementWrite } from '@/types';
import {
  BurgerQuizDetailCard,
  BurgerQuizForm,
  RoundStructure,
  QuizStructureEditor,
} from '@/features/quiz/components';
import {
  useBurgerQuizDetailQuery,
  useBurgerQuizStructureQuery,
  useUpdateBurgerQuizMutation,
  useUpdateBurgerQuizStructureMutation,
  useDeleteBurgerQuizMutation,
} from '@/features/quiz/hooks';

function formDataToPayload(data: BurgerQuizFormData) {
  return {
    title: data.title.trim(),
    toss: data.toss.trim(),
    tags: data.tags.length ? data.tags : undefined,
  };
}

export function BurgerQuizDetailEdit() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [apiFieldErrors, setApiFieldErrors] = useState<Record<string, string>>({});

  const {
    data: quiz,
    isLoading: quizLoading,
    isError: quizError,
    error: quizErrorObj,
  } = useBurgerQuizDetailQuery(id ?? '');
  const { data: structureData, isLoading: structureLoading } = useBurgerQuizStructureQuery(
    id ?? ''
  );
  const updateMutation = useUpdateBurgerQuizMutation();
  const updateStructureMutation = useUpdateBurgerQuizStructureMutation();
  const deleteMutation = useDeleteBurgerQuizMutation();

  const structure = structureData?.elements;
  const hasCustomStructure = (structure?.length ?? 0) > 0;

  const defaultFormValues = useMemo<Partial<BurgerQuizFormData>>(() => {
    if (!quiz) return {};
    return {
      title: quiz.title,
      toss: quiz.toss,
      tags: quiz.tags ?? [],
    };
  }, [quiz]);

  const effectiveStructure: BurgerQuizStructureElement[] = useMemo(() => {
    if (!quiz) return [];
    if (hasCustomStructure && structure) return structure;
    return quiz.structure ?? [];
  }, [hasCustomStructure, quiz, structure]);

  const handleEdit = () => setIsEditing(true);
  const handleCancelEdit = () => {
    setIsEditing(false);
    setApiFieldErrors({});
  };

  const handleSaveInfos = async (data: BurgerQuizFormData) => {
    if (!id || !quiz) return;
    setApiFieldErrors({});
    try {
      const payload = formDataToPayload(data);
      await updateMutation.mutateAsync({ id, payload });
      setIsEditing(false);
    } catch (error) {
      setApiFieldErrors(getApiFieldErrors(error));
    }
  };

  const handleSaveStructure = async (elements: BurgerQuizStructureElementWrite[]) => {
    if (!id) return;
    await updateStructureMutation.mutateAsync({ id, payload: { elements } });
  };

  const handleDeleteConfirm = async () => {
    if (!id) return;
    await deleteMutation.mutateAsync(id);
    navigate('..', { replace: true });
  };

  const { typography } = appTheme;

  if (!id) {
    navigate('..', { replace: true });
    return null;
  }

  if (quizLoading || !quiz) {
    return (
      <PageWrapper className="py-6 md:py-10">
        <p className={typography.body}>Chargement du quiz…</p>
      </PageWrapper>
    );
  }

  if (quizError) {
    return (
      <PageWrapper className="py-6 md:py-10">
        <p className="text-destructive">
          {getApiErrorMessage(quizErrorObj) ?? 'Impossible de charger le quiz.'}
        </p>
        <Button variant="outline" onClick={() => navigate('..')} className="mt-4">
          Retour
        </Button>
      </PageWrapper>
    );
  }

  return (
    <PageWrapper className="py-6 md:py-10 space-y-8">
      <ConfirmDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        title="Supprimer le Burger Quiz"
        description={`« ${quiz.title} » sera supprimé définitivement. Continuer ?`}
        confirmLabel="Supprimer"
        cancelLabel="Annuler"
        variant="destructive"
        onConfirm={handleDeleteConfirm}
        isLoading={deleteMutation.isPending}
      />

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <h1 className={typography.h2}>{quiz.title}</h1>
        <Button
          variant="outline"
          size="sm"
          className="text-destructive hover:bg-destructive/10 hover:text-destructive"
          onClick={() => setDeleteConfirmOpen(true)}
        >
          <Trash2 className="size-4" aria-hidden />
          Supprimer
        </Button>
      </div>

      {isEditing ? (
        <BurgerQuizForm
          defaultValues={defaultFormValues}
          onSubmit={handleSaveInfos}
          isLoading={updateMutation.isPending}
          submitLabel="Enregistrer"
          cancelLabel="Annuler"
          onCancel={handleCancelEdit}
          fieldErrors={apiFieldErrors}
        />
      ) : (
        <BurgerQuizDetailCard quiz={quiz} onEdit={handleEdit} />
      )}

      <RoundStructure quiz={quiz} />

      {structureLoading ? (
        <p className="text-sm text-muted-foreground">Chargement de la structure…</p>
      ) : (
        <QuizStructureEditor
          structure={effectiveStructure}
          onSave={handleSaveStructure}
          isLoading={updateStructureMutation.isPending}
          hasCustomStructure={hasCustomStructure}
        />
      )}
    </PageWrapper>
  );
}
