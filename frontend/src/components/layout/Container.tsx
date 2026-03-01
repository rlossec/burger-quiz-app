import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

interface ContainerProps {
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

export function Container({ children, className, size = 'xl' }: ContainerProps) {
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
