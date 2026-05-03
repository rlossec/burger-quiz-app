import { colors } from '../colors';

const INGREDIENTS = ['🍔', '🧀', '🥬', '🍅', '🧅', '🥩', '🍟', '🥤', '🌭', '🫙'];

interface Particle {
  id: number;
  emoji: string;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
  rotation: number;
  drift: number;
  opacity: number;
}

function seededRandom(seed: number): number {
  const x = Math.sin(seed * 9999) * 10000;
  return x - Math.floor(x);
}

function generateParticles(count: number): Particle[] {
  return Array.from({ length: count }, (_, i) => {
    const seed = i + 1;
    return {
      id: i,
      emoji: INGREDIENTS[i % INGREDIENTS.length],
      x: seededRandom(seed) * 100,
      y: seededRandom(seed * 2) * 100,
      size: 18 + seededRandom(seed * 3) * 22,
      duration: 12 + seededRandom(seed * 4) * 16,
      delay: seededRandom(seed * 5) * -20,
      rotation: seededRandom(seed * 6) * 360,
      drift: (seededRandom(seed * 7) - 0.5) * 40,
      opacity: 0.12 + seededRandom(seed * 8) * 0.1,
    };
  });
}

const PARTICLES = generateParticles(14);

/**
 * Overlay grain SVG pour texture subtile
 */
export function GrainOverlay() {
  return (
    <svg
      className="pointer-events-none fixed inset-0 z-1 h-full w-full opacity-[0.035]"
      aria-hidden="true"
    >
      <filter id="grain">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.65"
          numOctaves="3"
          stitchTiles="stitch"
        />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter="url(#grain)" />
    </svg>
  );
}

/**
 * Blobs colorés animés en arrière-plan
 */
export function BackgroundBlobs() {
  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden" aria-hidden="true">
      {/* Ketchup blob */}
      <div
        className="absolute -left-32 -top-32 h-[500px] w-[500px] rounded-full opacity-20 blur-3xl"
        style={{
          background: colors.ketchup,
          animation: 'blob1 18s ease-in-out infinite alternate',
        }}
      />
      {/* Mustard blob */}
      <div
        className="absolute -right-32 top-1/3 h-[420px] w-[420px] rounded-full opacity-15 blur-3xl"
        style={{
          background: colors.mustard,
          animation: 'blob2 22s ease-in-out infinite alternate',
        }}
      />
      {/* Denim blob */}
      <div
        className="absolute bottom-0 left-1/3 h-[380px] w-[380px] rounded-full opacity-15 blur-3xl"
        style={{
          background: colors.denim,
          animation: 'blob3 16s ease-in-out infinite alternate',
        }}
      />
      {/* Lettuce blob */}
      <div
        className="absolute -bottom-20 right-0 h-[300px] w-[300px] rounded-full opacity-10 blur-3xl"
        style={{
          background: colors.lettuce,
          animation: 'blob1 20s ease-in-out infinite alternate-reverse',
        }}
      />
    </div>
  );
}

/**
 * Particules flottantes
 */
export function FloatingParticles() {
  return (
    <div className="pointer-events-none fixed inset-0 z-2 overflow-hidden" aria-hidden="true">
      {PARTICLES.map((p) => (
        <span
          key={p.id}
          className="absolute select-none"
          style={
            {
              left: `${p.x}%`,
              top: `${p.y}%`,
              fontSize: `${p.size}px`,
              opacity: p.opacity,
              animation: `float ${p.duration}s ${p.delay}s ease-in-out infinite alternate`,
              transform: `rotate(${p.rotation}deg)`,
              '--drift': `${p.drift}px`,
              filter: 'blur(0.3px)',
            } as React.CSSProperties
          }
        >
          {p.emoji}
        </span>
      ))}
    </div>
  );
}

/**
 * Wrapper combinant tous les effets de fond
 */
export function ThemeBackground() {
  return (
    <>
      <BackgroundBlobs />
      <FloatingParticles />
      <GrainOverlay />
    </>
  );
}
