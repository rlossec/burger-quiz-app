import { ThemeProvider } from './theme';
import { QueryProvider } from './QueryProvider';

interface AppProvidersProps {
  children: React.ReactNode;
}

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem disableTransitionOnChange>
      <QueryProvider>{children}</QueryProvider>
    </ThemeProvider>
  );
}
