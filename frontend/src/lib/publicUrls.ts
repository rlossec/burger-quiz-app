/**
 * Définition des endpoints publics (sans token JWT requis).
 * Chaque entrée peut matcher par méthode HTTP + pattern d'URL.
 * Si `methods` est absent, toutes les méthodes sont considérées publiques.
 */
const PUBLIC_ENDPOINTS: Array<{
  pattern: RegExp;
  methods?: string[];
}> = [
  // Auth JWT
  { pattern: /\/auth\/jwt\/create\// }, // login
  { pattern: /\/auth\/jwt\/refresh\// }, // refresh (appelé par l'interceptor lui-même)

  // Djoser — gestion du compte
  { pattern: /\/auth\/users\/activation\// },
  { pattern: /\/auth\/users\/resend_activation\// },
  { pattern: /\/auth\/users\/reset_password\// },
  { pattern: /\/auth\/users\/reset_password_confirm\// },
  { pattern: /\/auth\/users\/reset_username\// },
  { pattern: /\/auth\/users\/reset_username_confirm\// },

  // Inscription : POST /auth/users/ uniquement
  // GET /auth/users/ est protégé (liste admin)
  { pattern: /\/auth\/users\/$/, methods: ['POST'] },
];

/**
 * Vérifie si une URL + méthode correspond à un endpoint public.
 * Utilisé par les interceptors axios pour ignorer la gestion des tokens.
 */
export const isPublicUrl = (url?: string, method?: string): boolean => {
  if (!url) return false;

  return PUBLIC_ENDPOINTS.some(({ pattern, methods }) => {
    if (!pattern.test(url)) return false;
    if (!methods) return true;
    return methods.includes((method ?? '').toUpperCase());
  });
};
