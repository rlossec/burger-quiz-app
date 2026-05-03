import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { PageWrapper } from '@/components/layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { appTheme } from '@/theme';
import { getApiFieldErrors } from '@/lib/api-error';
import type { BurgerQuizFormData } from '@/features/quiz/schemas/burger-quiz';
import { BurgerQuizForm } from '@/features/quiz/components';
import { useCreateBurgerQuizMutation } from '@/features/quiz/hooks';

function formDataToPayload(data: BurgerQuizFormData) {
  return {
    title: data.title.trim(),
    toss: data.toss.trim(),
    tags: data.tags.length ? data.tags : undefined,
  };
}

export function BurgerQuizCreatePage() {
  const navigate = useNavigate();
  const createMutation = useCreateBurgerQuizMutation();
  const [apiFieldErrors, setApiFieldErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (data: BurgerQuizFormData) => {
    setApiFieldErrors({});
    try {
      const payload = formDataToPayload(data);
      const created = await createMutation.mutateAsync(payload);
      navigate(`/quiz/${created.id}`, { replace: true });
    } catch (error) {
      setApiFieldErrors(getApiFieldErrors(error));
    }
  };

  const handleCancel = () => {
    navigate('..');
  };

  const { typography } = appTheme;

  return (
    <PageWrapper className="py-6 md:py-10">
      <Card>
        <CardHeader className="border-b">
          <CardTitle className={typography.h2}>Créer un Burger Quiz</CardTitle>
        </CardHeader>
        <CardContent className="pt-6">
          <BurgerQuizForm
            onSubmit={handleSubmit}
            isLoading={createMutation.isPending}
            submitLabel="Créer"
            cancelLabel="Annuler"
            onCancel={handleCancel}
            fieldErrors={apiFieldErrors}
          />
        </CardContent>
      </Card>
    </PageWrapper>
  );
}
