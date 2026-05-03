import { z } from 'zod';

export const burgerQuizFormSchema = z.object({
  title: z.string().min(1, 'Le titre est obligatoire'),
  toss: z.string().min(1, 'Le toss est obligatoire'),
  tags: z.array(z.string().trim().min(3).max(32)).max(15),
});

export type BurgerQuizFormData = z.infer<typeof burgerQuizFormSchema>;
