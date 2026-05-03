/**
 * Palette de couleurs
 *
 */

export const colors = {
  // Couleurs principales
  ketchup: 'oklch(0.5 0.18 25)',
  ketchupLight: 'oklch(0.58 0.2 25)',
  mustard: 'oklch(0.85 0.17 90)',
  denim: 'oklch(0.6 0.1 260)',
  denimLight: 'oklch(0.65 0.12 260)',
  bun: 'oklch(0.72 0.14 60)',
  patty: 'oklch(0.35 0.06 45)',
  lettuce: 'oklch(0.58 0.14 135)',
  onion: 'oklch(0.48 0.12 340)',

  // Neutres
  dark: 'oklch(0.15 0.01 50)',
  darkAlt: 'oklch(0.12 0.01 50)',
  cream: 'oklch(0.95 0.015 85)',
  creamDark: 'oklch(0.92 0.015 85)',

  // Transparences courantes
  transparent: {
    cream5: 'oklch(0.95 0.015 85 / 0.05)',
    cream8: 'oklch(0.95 0.015 85 / 0.08)',
    cream10: 'oklch(0.95 0.015 85 / 0.1)',
    cream12: 'oklch(0.95 0.015 85 / 0.12)',
    dark85: 'oklch(0.15 0.01 50 / 0.85)',
    ketchup40: 'oklch(0.5 0.18 25 / 0.4)',
    mustard40: 'oklch(0.85 0.17 90 / 0.4)',
    denim40: 'oklch(0.6 0.1 260 / 0.4)',
    denim15: 'oklch(0.6 0.1 260 / 0.15)',
    denim35: 'oklch(0.6 0.1 260 / 0.35)',
    denim45: 'oklch(0.6 0.1 260 / 0.45)',
  },
} as const;

export type ThemeColors = typeof colors;
