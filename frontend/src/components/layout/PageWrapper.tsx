import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

interface PageWrapperProps {
  children: React.ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
}

const sizeClasses = {
  sm: 'max-w-screen-sm',
  md: 'max-w-screen-md',
  lg: 'max-w-screen-lg',
  xl: 'max-w-screen-xl',
  full: 'max-w-full',
};

/**
 * Conteneur de mise en page : largeur max, padding horizontal.
 * Réutilisable dans layout, pages, etc.
 */
export function PageWrapper({ children, className, size = 'xl' }: PageWrapperProps) {
  return (
    <div
      className={cn(
        'mx-auto w-full',
        appTheme.spacing.container.padding,
        sizeClasses[size],
        className
      )}
    >
      {children}
    </div>
  );
}
