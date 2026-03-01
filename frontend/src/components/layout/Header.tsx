import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Menu, X, User, LogIn } from 'lucide-react';

import { Container } from './Container';
import { Nav } from './Nav';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { layout, separators, logo, mobileMenu, buttons } = appTheme;

  // TODO: Remplacer par le vrai état d'authentification
  const isAuthenticated = false;

  return (
    <header className="sticky top-0 z-50 w-full">
      <div className={cn('shadow-lg', layout.headerBg)}>
        <Container>
          <div className="flex h-16 items-center justify-between gap-4">
            {/* Logo - gauche */}
            <Link
              to="/"
              className="group flex shrink-0 items-center gap-3 transition-transform hover:scale-105"
            >
              <div
                className={cn(
                  'flex h-12 w-12 items-center justify-center rounded-full text-3xl shadow-inner',
                  logo.icon.bg,
                  logo.icon.ring
                )}
              >
                🍔
              </div>
              <div className="hidden flex-col leading-none sm:flex">
                <span
                  className={cn('text-2xl font-black tracking-tight drop-shadow-sm', logo.burger)}
                >
                  BURGER
                </span>
                <span className={cn('text-sm font-extrabold tracking-[0.3em]', logo.quiz)}>
                  QUIZ
                </span>
              </div>
            </Link>

            {/* Navigation desktop - centre (lg+) */}
            <Nav className="hidden lg:flex" />

            {/* Zone droite : Auth + Menu mobile */}
            <div className="flex items-center gap-2">
              {/* Auth desktop (md+) */}
              <div className="hidden items-center gap-2 md:flex">
                {isAuthenticated ? (
                  <Button variant="ghost" size="sm" className={mobileMenu.button} asChild>
                    <Link to="/profile">
                      <User className="mr-2 h-4 w-4" />
                      Profil
                    </Link>
                  </Button>
                ) : (
                  <>
                    <Button variant="ghost" size="sm" className={mobileMenu.button} asChild>
                      <Link to="/login">
                        <LogIn className="mr-2 h-4 w-4" />
                        Connexion
                      </Link>
                    </Button>
                    <Button size="sm" className={buttons.primary} asChild>
                      <Link to="/register">S'inscrire</Link>
                    </Button>
                  </>
                )}
              </div>

              {/* Navigation tablette (md mais pas lg) */}
              <Nav className="hidden md:flex lg:hidden" />

              {/* Menu mobile toggle */}
              <button
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className={cn(
                  'flex h-10 w-10 items-center justify-center rounded-lg transition-colors md:hidden',
                  mobileMenu.button
                )}
                aria-label={mobileMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'}
              >
                {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </button>
            </div>
          </div>
        </Container>
      </div>

      {/* Menu mobile déroulant */}
      <div
        className={cn(
          'overflow-hidden transition-all duration-300 md:hidden',
          layout.headerBg,
          mobileMenuOpen ? 'max-h-96' : 'max-h-0'
        )}
      >
        <Container>
          <div className="space-y-4 py-4">
            {/* Navigation mobile */}
            <Nav
              className="flex-col items-stretch gap-1"
              onNavigate={() => setMobileMenuOpen(false)}
            />

            {/* Séparateur */}
            <div className="border-t border-cream/10" />

            {/* Auth mobile */}
            <div className="flex flex-col gap-2">
              {isAuthenticated ? (
                <Button variant="ghost" className={mobileMenu.button} asChild>
                  <Link to="/profile" onClick={() => setMobileMenuOpen(false)}>
                    <User className="mr-2 h-4 w-4" />
                    Mon profil
                  </Link>
                </Button>
              ) : (
                <>
                  <Button variant="ghost" className={mobileMenu.button} asChild>
                    <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                      <LogIn className="mr-2 h-4 w-4" />
                      Connexion
                    </Link>
                  </Button>
                  <Button className={buttons.primary} asChild>
                    <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                      S'inscrire
                    </Link>
                  </Button>
                </>
              )}
            </div>
          </div>
        </Container>
      </div>

      {/* Séparateur lumineux */}
      <div
        className={cn(separators.header.height, separators.header.color, separators.header.glow)}
      />
    </header>
  );
}
