import { cn } from '@/lib/utils';
import { appTheme } from '@/theme';

interface PagePlaceholderProps {
  name: string;
}

export function PagePlaceholder({ name }: PagePlaceholderProps) {
  const { typography, text, cards } = appTheme;

  return (
    <div className={cn('flex min-h-[50vh] items-center justify-center rounded-2xl', cards.default)}>
      <h1 className={cn(typography.h2, text.primary)}>{name}</h1>
    </div>
  );
}
