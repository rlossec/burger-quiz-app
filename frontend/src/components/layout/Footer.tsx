import { Link } from 'react-router-dom';
import { PageWrapper } from './PageWrapper';
import { colors } from '@/theme';

/**
 * Footer — "pain du bas" du burger.
 *
 * Fond : dégradé dark → patty (symétrique du Header qui fait patty → dark).
 * Le séparateur Onion est positionné AVANT le footer dans Layout.tsx,
 * jouant le rôle de la "couche oignon" entre le contenu et le pain du bas.
 */
export function Footer() {
  return (
    <footer
      className="relative mt-auto"
      style={{
        background: `linear-gradient(to bottom, ${colors.dark}, ${colors.patty}cc, ${colors.patty})`,
      }}
    >
      <PageWrapper>
        <div className="grid gap-8 py-8 sm:py-10 md:grid-cols-3 lg:py-12">
          {/* Logo + description */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <span className="text-2xl sm:text-3xl">🍔</span>
              <div className="flex flex-col leading-none">
                <span
                  className="text-lg font-black tracking-tight sm:text-xl"
                  style={{ color: colors.bun, fontFamily: "'Syne', system-ui" }}
                >
                  BURGER
                </span>
                <span
                  className="text-xs font-extrabold tracking-[0.2em]"
                  style={{ color: `${colors.bun}cc`, fontFamily: "'Syne', system-ui" }}
                >
                  QUIZ
                </span>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <div className="space-y-3 sm:space-y-4">
            <h3
              className="text-lg font-semibold"
              style={{ color: colors.bun, fontFamily: "'Syne', system-ui" }}
            >
              Navigation
            </h3>
            <nav className="flex flex-col gap-2 text-sm">
              {[
                { to: '/', label: 'Accueil' },
                { to: '/quiz', label: 'Mes Quiz' },
                { to: '/play', label: 'Jouer' },
              ].map(({ to, label }) => (
                <Link key={to} to={to} className="text-cream/60 hover:text-onion transition-colors">
                  {label}
                </Link>
              ))}
            </nav>
          </div>

          {/* Liens */}
          <div className="space-y-3 sm:space-y-4">
            <h3
              className="text-lg font-semibold"
              style={{ color: colors.bun, fontFamily: "'Syne', system-ui" }}
            >
              Liens
            </h3>
            <nav className="flex flex-col gap-2 text-sm">
              <a
                href="https://github.com/rlossec/burger-quiz-app"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-cream/60 hover:text-onion transition-colors"
              >
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    fillRule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                    clipRule="evenodd"
                  />
                </svg>
                GitHub
              </a>
            </nav>
          </div>
        </div>

        {/* Copyright */}
        <div
          className="flex items-center justify-center border-t py-4 text-sm sm:py-6"
          style={{
            borderColor: `${colors.cream}1a`,
            color: `${colors.cream}80`,
            fontFamily: "'DM Sans', system-ui",
          }}
        >
          <p>Rlossec</p>
        </div>
      </PageWrapper>
    </footer>
  );
}
