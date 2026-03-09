import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { PageWrapper } from './PageWrapper';
import { Nav } from './Nav';

import { colors } from '@/theme';
import { useAuthStore } from '@/stores';
import { tokenStorage } from '@/lib/axios';
import { Logo } from './header/Logo';
import { HeaderUserActions } from './header/HeaderUserActions';
import { MobileMenuToggle } from './header/MobileMenuToggle';
import { MobileMenuPanel } from './header/MobileMenuPanel';

/**
 * En-tête — "chapeau du pain" du burger.
 *
 * Fond : dégradé patty → dark (cohérent avec Footer qui fait dark → patty).
 * Le séparateur Lettuce est positionné APRÈS le header dans Layout.tsx.
 */
export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    tokenStorage.clear();
    setMobileMenuOpen(false);
    navigate('/auth/login');
  };

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <header className="sticky top-0 z-50 w-full">
      {/* Corps du header */}
      <div
        className="shadow-lg"
        style={{
          background: `linear-gradient(to bottom, ${colors.patty}, ${colors.patty}cc, ${colors.dark})`,
        }}
      >
        <PageWrapper>
          <div className="flex h-16 items-center justify-between gap-4">
            <Logo />

            {isAuthenticated && <Nav className="hidden lg:flex" />}

            <div className="flex items-center gap-3">
              {isAuthenticated ? (
                <>
                  <Nav className="hidden md:flex lg:hidden" />
                  <HeaderUserActions
                    username={user?.username}
                    onLogout={handleLogout}
                    variant="desktop"
                  />
                  <MobileMenuToggle
                    open={mobileMenuOpen}
                    onToggle={() => setMobileMenuOpen(!mobileMenuOpen)}
                  />
                </>
              ) : null}
            </div>
          </div>
        </PageWrapper>
      </div>

      {isAuthenticated && (
        <MobileMenuPanel
          open={mobileMenuOpen}
          username={user?.username}
          onLogout={handleLogout}
          onNavigate={closeMobileMenu}
        />
      )}
    </header>
  );
}
