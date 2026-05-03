import { colors, fonts } from '@/theme';

const DEFAULT_BADGES = [
  { icon: '🎙️', label: 'Discord' },
  { icon: '🏆', label: 'Quiz Live' },
  { icon: '🎭', label: 'Animations' },
] as const;

type StatsBadgesProps = {
  badges?: ReadonlyArray<{ icon: string; label: string }>;
  className?: string;
};

/**
 * Badges de stats / features (Discord, Quiz Live, etc.).
 * Réutilisable dans auth, landing, etc.
 */
export function StatsBadges({ badges = DEFAULT_BADGES, className }: StatsBadgesProps) {
  return (
    <div
      className={className}
      style={{ animation: 'entrance 0.7s 0.3s cubic-bezier(0.22, 1, 0.36, 1) both' }}
    >
      <div className="flex gap-3">
        {badges.map(({ icon, label }) => (
          <div
            key={label}
            className="flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium text-cream/80"
            style={{
              background: colors.transparent.cream8,
              border: `1px solid ${colors.transparent.cream12}`,
            }}
          >
            <span>{icon}</span>
            <span style={{ fontFamily: fonts.body }}>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
