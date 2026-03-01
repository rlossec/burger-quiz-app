import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Footer } from './Footer';
import { Container } from './Container';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

export function Layout() {
  return (
    <div
      className={cn('flex min-h-screen flex-col', appTheme.layout.mainBg, appTheme.layout.mainText)}
    >
      <Header />

      <main className="relative flex-1">
        <Container className="py-8 md:py-12">
          <Outlet />
        </Container>
      </main>

      <Footer />
    </div>
  );
}
