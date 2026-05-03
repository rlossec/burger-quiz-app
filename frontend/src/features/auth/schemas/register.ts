import { z } from 'zod';

export const registerSchema = z
  .object({
    username: z
      .string()
      .min(3, "L'identifiant doit contenir au moins 3 caractères")
      .max(30, "L'identifiant ne peut pas dépasser 30 caractères")
      .regex(
        /^[a-zA-Z0-9_]+$/,
        "L'identifiant ne peut contenir que des lettres, chiffres et underscores"
      ),
    email: z.email('Adresse email invalide'),
    password: z
      .string()
      .min(8, 'Le mot de passe doit contenir au moins 8 caractères')
      .regex(/[A-Z]/, 'Le mot de passe doit contenir au moins une majuscule')
      .regex(/[a-z]/, 'Le mot de passe doit contenir au moins une minuscule')
      .regex(/[0-9]/, 'Le mot de passe doit contenir au moins un chiffre'),
    re_password: z.string(),
  })
  .refine((data) => data.password === data.re_password, {
    message: 'Les mots de passe ne correspondent pas',
    path: ['re_password'],
  });

export type RegisterFormData = z.infer<typeof registerSchema>;
