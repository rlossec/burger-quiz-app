import { colors } from '@/theme';

export function BurgerArtwork() {
  return (
    <div
      className="relative flex flex-col items-center"
      style={{ animation: 'entrance 0.7s cubic-bezier(0.22, 1, 0.36, 1) both' }}
    >
      <div className="flex flex-col items-center gap-0 leading-none select-none">
        <span
          style={{
            fontSize: 90,
            filter: 'drop-shadow(0 8px 24px rgba(0,0,0,0.4))',
            animation: 'floatSlow 6s ease-in-out infinite alternate',
          }}
        >
          🍔
        </span>
      </div>

      {/* Decorative ring */}
      <div
        className="absolute inset-0 -m-8 rounded-full border-2 border-dashed opacity-20"
        style={{ borderColor: colors.mustard, animation: 'spin 30s linear infinite' }}
      />
      <div
        className="absolute inset-0 -m-16 rounded-full border border-dashed opacity-10"
        style={{
          borderColor: colors.ketchup,
          animation: 'spin 50s linear infinite reverse',
        }}
      />
    </div>
  );
}
