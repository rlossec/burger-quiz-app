import { colors, fonts } from '@/theme';

const DEFAULT_SUBTITLE = 'Créez et animez vos émissions quiz en vocal sur Discord.';

type ArtworkSubtitleProps = {
  subtitle?: string;
};

export function ArtworkSubtitle({ subtitle = DEFAULT_SUBTITLE }: ArtworkSubtitleProps) {
  return (
    <div
      className="space-y-3 text-center"
      style={{ animation: 'entrance 0.7s 0.15s cubic-bezier(0.22, 1, 0.36, 1) both' }}
    >
      <h1
        className="font-black tracking-tight text-cream"
        style={{
          fontSize: 'clamp(2rem, 3vw, 3.5rem)',
          fontFamily: fonts.heading,
          letterSpacing: '-0.02em',
        }}
      >
        <span style={{ color: colors.ketchupLight }}>Burger</span>{' '}
        <span style={{ color: colors.mustard }}>Quiz</span>
      </h1>
      <p
        className="mx-auto max-w-xs text-lg leading-relaxed text-cream/60"
        style={{ fontFamily: fonts.body }}
      >
        {subtitle}
      </p>
    </div>
  );
}
