import { Link } from 'react-router-dom';
import { colors } from '@/theme';

/**
 * Logo Burger Quiz — lien vers l'accueil.
 * Icône 🍔 + typo BURGER / QUIZ.
 */
export function Logo() {
  return (
    <Link
      to="/"
      className="group flex shrink-0 items-center gap-3 transition-transform hover:scale-105"
    >
      <div
        className="flex h-12 w-12 items-center justify-center rounded-full text-3xl shadow-inner"
        style={{
          background: `${colors.bun}33`,
          boxShadow: `0 0 0 2px ${colors.bun}4d`,
        }}
      >
        🍔
      </div>
      <div className="hidden flex-col leading-none sm:flex">
        <span
          className="text-2xl font-black tracking-tight drop-shadow-sm"
          style={{ color: colors.bun, fontFamily: "'Syne', system-ui" }}
        >
          BURGER
        </span>
        <span
          className="text-sm font-extrabold tracking-[0.3em]"
          style={{ color: `${colors.bun}cc`, fontFamily: "'Syne', system-ui" }}
        >
          QUIZ
        </span>
      </div>
    </Link>
  );
}
