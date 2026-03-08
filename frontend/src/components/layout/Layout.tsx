import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Footer } from './Footer';
import { PageWrapper } from './PageWrapper';
import { LettuceSeparator, OnionSeparator } from '@/components/ui/custom/separators';
import { cn } from '@/lib/utils';
import { colors, ThemeBackground } from '@/theme';

export function Layout() {
  return (
    <div
      className={cn('relative flex min-h-screen flex-col text-cream')}
      style={{ background: colors.darkAlt }}
    >
      {/* Couche background partagée (blobs + particules + grain) */}
      <ThemeBackground />

      {/* Couche contenu */}
      <div className="relative z-10 flex min-h-screen flex-col">
        <Header />
        <LettuceSeparator />
        {/* ── Contenu principal ── */}
        <main className="relative flex-1">
          <PageWrapper className="py-8 md:py-12">
            <Outlet />
          </PageWrapper>
        </main>
        <OnionSeparator />
        <Footer />
      </div>
    </div>
  );
}
