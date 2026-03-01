import { Link } from 'react-router-dom';
import { Github } from 'lucide-react';
import { Container } from './Container';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

export function Footer() {
  const { layout, separators, logo, footer, typography } = appTheme;

  return (
    <footer className={cn('relative mt-auto', layout.footerBg)}>
      {/* Séparateur lumineux */}
      <div
        className={cn(separators.footer.height, separators.footer.color, separators.footer.glow)}
      />

      <Container>
        <div className="grid gap-8 py-8 sm:py-10 md:grid-cols-3 lg:py-12">
          {/* Logo et description */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <span className="text-2xl sm:text-3xl">🍔</span>
              <div className="flex flex-col leading-none">
                <span className={cn('text-lg font-black tracking-tight sm:text-xl', logo.burger)}>
                  BURGER
                </span>
                <span className={cn('text-xs font-extrabold tracking-[0.2em]', logo.quiz)}>
                  QUIZ
                </span>
              </div>
            </div>
            <p className={cn(typography.small, footer.text)}>
              Créez et jouez à vos propres quiz dans l'esprit du célèbre jeu télévisé.
            </p>
          </div>

          {/* Navigation */}
          <div className="space-y-3 sm:space-y-4">
            <h3 className={cn(typography.h4, footer.title)}>Navigation</h3>
            <nav className={cn('flex flex-col gap-2', typography.small)}>
              <Link to="/" className={cn('transition-colors', footer.link)}>
                Accueil
              </Link>
              <Link to="/quiz" className={cn('transition-colors', footer.link)}>
                Mes Quiz
              </Link>
              <Link to="/play" className={cn('transition-colors', footer.link)}>
                Jouer
              </Link>
            </nav>
          </div>

          {/* Liens externes */}
          <div className="space-y-3 sm:space-y-4">
            <h3 className={cn(typography.h4, footer.title)}>Liens</h3>
            <nav className={cn('flex flex-col gap-2', typography.small)}>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className={cn('flex items-center gap-2 transition-colors', footer.link)}
              >
                <Github className="h-4 w-4" />
                GitHub
              </a>
            </nav>
          </div>
        </div>

        {/* Copyright */}
        <div
          className={cn(
            'flex items-center justify-center border-t py-4 sm:py-6',
            typography.small,
            footer.border,
            footer.copyright
          )}
        >
          <p>Rlossec</p>
        </div>
      </Container>
    </footer>
  );
}
