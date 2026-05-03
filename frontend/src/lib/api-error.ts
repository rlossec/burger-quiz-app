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
