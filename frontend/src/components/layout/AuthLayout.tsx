import { useOutlet } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { colors, fonts, ThemeBackground } from '@/theme';
import { BurgerArtwork, ArtworkSubtitle } from '../common/artwork';
import { StatsBadges } from '@/components/ui/custom/StatsBadges';

// ─── AuthLayout ──────────────────────────────────────────────────────────────
interface AuthLayoutProps {
  children?: React.ReactNode;
  className?: string;
}

export function AuthLayout({ children, className }: AuthLayoutProps) {
  const outlet = useOutlet();
  const content = children ?? outlet;

  return (
    <div
      className={cn('relative min-h-screen w-full overflow-hidden', className)}
      style={{ background: colors.darkAlt, fontFamily: fonts.body }}
    >
      {/* Background effects */}
      <ThemeBackground />

      {/* Two-column layout */}
      <div className="relative z-10 flex min-h-screen">
        {/* Left: artwork (desktop only) */}
        <div className="relative z-10 hidden lg:flex lg:w-[45%] lg:flex-col lg:items-center lg:justify-center lg:gap-8 lg:p-12 lg:border-r lg:border-cream/5">
          <BurgerArtwork />
          <ArtworkSubtitle />
          <StatsBadges />
        </div>

        {/* Right: form */}
        <div className="flex w-full flex-col items-center justify-center px-4 py-12 lg:w-[55%] lg:px-12">
          {/* Mobile logo */}
          <div
            className="mb-8 flex flex-col items-center gap-2 lg:hidden"
            style={{ animation: 'entrance 0.5s cubic-bezier(0.22, 1, 0.36, 1) both' }}
          >
            <span
              className="text-6xl"
              style={{ animation: 'floatSlow 5s ease-in-out infinite alternate' }}
            >
              🍔
            </span>
            <span
              className="font-black text-2xl tracking-tight"
              style={{ fontFamily: "'Syne', system-ui" }}
            >
              <span style={{ color: colors.ketchupLight }}>Burger</span>{' '}
              <span style={{ color: colors.mustard }}>Quiz</span>
            </span>
          </div>

          {/* Card */}
          <div
            className="w-full max-w-md rounded-2xl overflow-hidden"
            style={{
              animation: 'cardIn 0.6s cubic-bezier(0.22, 1, 0.36, 1) both',
              background: colors.transparent.dark85,
              border: `1px solid ${colors.transparent.cream10}`,
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
            }}
          >
            {/* Separator gradient */}
            <div
              className="h-0.5"
              style={{
                background: `linear-gradient(90deg,
                  transparent,
                  ${colors.transparent.ketchup40} 20%,
                  ${colors.transparent.mustard40} 50%,
                  ${colors.transparent.denim40} 80%,
                  transparent
                )`,
              }}
            />
            <div className="p-8">{content}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
