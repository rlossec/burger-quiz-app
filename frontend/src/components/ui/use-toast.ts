/**
 * Hook toast minimal — interface compatible avec shadcn/ui useToast.
 * Remplacer par une implémentation réelle (sonner, radix, etc.) si besoin d'affichage.
 */
export interface ToastOptions {
  title: string;
  description?: string;
  variant?: 'default' | 'destructive';
}

export function useToast() {
  const toast = (options: ToastOptions) => {
    if (import.meta.env.DEV) {
      const msg = options.description ? `${options.title}: ${options.description}` : options.title;
      if (options.variant === 'destructive') {
        console.warn('[toast]', msg);
      } else {
        console.log('[toast]', msg);
      }
    }
  };
  return { toast };
}
