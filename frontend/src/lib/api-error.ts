import { AxiosError } from 'axios';

/**
 * Extrait un message lisible depuis une erreur Axios.
 * Gère les formats de réponses typiques Django REST :
 * - { detail: "..." }
 * - { field: ["message"] }
 * - String brute.
 */
export const getApiErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    const data = error.response?.data;
    if (!data) return error.message;

    if (typeof data === 'string') return data;
    if (typeof data.detail === 'string') return data.detail;

    // Erreurs de validation
    const firstKey = Object.keys(data)[0];
    if (firstKey) {
      const val = data[firstKey];
      return Array.isArray(val) ? `${firstKey} : ${val[0]}` : String(val);
    }
  }
  return 'Une erreur inattendue est survenue.';
};

/**
 * Extrait les erreurs par champ depuis une réponse 400 (validation Django REST).
 * Retourne un objet { fieldName: "premier message" } pour chaque champ en erreur.
 */
export const getApiFieldErrors = (error: unknown): Record<string, string> => {
  if (error instanceof AxiosError && error.response?.status === 400) {
    const data = error.response.data;
    if (
      data &&
      typeof data === 'object' &&
      !Array.isArray(data) &&
      typeof data.detail !== 'string'
    ) {
      const out: Record<string, string> = {};
      for (const key of Object.keys(data)) {
        const val = (data as Record<string, unknown>)[key];
        if (Array.isArray(val) && val[0]) {
          out[key] = String(val[0]);
        } else if (typeof val === 'string') {
          out[key] = val;
        }
      }
      return out;
    }
  }
  return {};
};
