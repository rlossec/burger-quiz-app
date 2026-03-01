/**
 * Configuration du thème Burger Quiz
 *
 * Structure modulaire pour faciliter les évolutions futures.
 * Les couleurs de base (ketchup, mustard, etc.) sont définies dans App.css
 * via les variables CSS et exposées à Tailwind.
 *
 * Opacités standards utilisées :
 * - /10 : backgrounds très subtils
 * - /20 : hover léger, ghost buttons
 * - /30 : états actifs
 * - /50 : borders, textes tertiaires
 * - /60 : textes muted
 * - /70 : textes inactifs
 * - /80 : gradients, textes secondaires
 * - /90 : hover buttons
 */

export const appTheme = {
  name: 'burger-quiz',

  // Breakpoints (référence, valeurs Tailwind par défaut)
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Spacing - tailles standards
  spacing: {
    container: {
      padding: 'px-4 sm:px-6 lg:px-8',
      maxWidth: 'max-w-7xl',
    },
    section: {
      padding: 'p-4 sm:p-6 md:p-8',
      paddingY: 'py-8 md:py-12 lg:py-16',
      gap: 'gap-6 md:gap-8 lg:gap-12',
    },
    card: {
      padding: 'p-4 sm:p-6',
      gap: 'gap-4 sm:gap-6',
    },
  },

  // Typography - tailles responsive
  typography: {
    h1: 'text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black tracking-tight',
    h2: 'text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight',
    h3: 'text-xl sm:text-2xl font-bold',
    h4: 'text-lg sm:text-xl font-semibold',
    body: 'text-base',
    bodyLarge: 'text-lg md:text-xl',
    small: 'text-sm',
    xs: 'text-xs',
  },

  // Layout - Fonds et textes principaux
  layout: {
    headerBg: 'bg-linear-to-b from-patty via-patty/80 to-dark',
    footerBg: 'bg-linear-to-t from-patty via-patty/80 to-dark',
    mainBg: 'bg-linear-to-b from-dark via-onion/10 to-dark',
    mainText: 'text-cream',
  },

  // Séparateurs
  separators: {
    header: {
      color: 'bg-lettuce',
      glow: 'shadow-[0_4px_12px_rgba(76,175,80,0.6),0_2px_4px_rgba(76,175,80,0.8)]',
      height: 'h-1',
    },
    footer: {
      color: 'bg-onion',
      glow: 'shadow-[0_-4px_12px_rgba(156,39,176,0.5),0_-2px_4px_rgba(156,39,176,0.7)]',
      height: 'h-1',
    },
  },

  // Textes
  text: {
    primary: 'text-cream',
    secondary: 'text-cream/80',
    muted: 'text-cream/60',
    inactive: 'text-cream/70',
    subtle: 'text-cream/50',
    accent: {
      ketchup: 'text-ketchup',
      mayo: 'text-mustard',
      bun: 'text-bun',
      denim: 'text-denim',
      onion: 'text-onion',
      lettuce: 'text-lettuce',
    },
  },

  // Logo
  logo: {
    icon: {
      bg: 'bg-bun/20',
      ring: 'ring-2 ring-bun/30',
    },
    burger: 'text-bun',
    quiz: 'text-bun/80',
  },

  // Navigation
  nav: {
    active: 'bg-denim/30 text-cream shadow-sm',
    inactive: 'text-cream/70',
    hover: 'hover:bg-cream/10 hover:text-bun',
  },

  // Boutons mobile
  mobileMenu: {
    button: 'bg-cream/10 text-cream hover:bg-cream/20',
  },

  // Footer
  footer: {
    title: 'text-bun',
    text: 'text-cream/60',
    link: 'text-cream/60 hover:text-onion',
    border: 'border-cream/10',
    copyright: 'text-cream/50',
  },

  // Boutons
  buttons: {
    primary: 'bg-denim text-cream hover:bg-denim/90',
    secondary: 'bg-onion text-cream hover:bg-onion/90',
    outline: {
      ketchup: 'border-2 border-ketchup bg-transparent text-cream hover:bg-ketchup/20',
      mayo: 'border-2 border-mustard bg-transparent text-cream hover:bg-mustard/20',
      denim: 'border-2 border-denim bg-transparent text-cream hover:bg-denim/20',
      onion: 'border-2 border-onion bg-transparent text-cream hover:bg-onion/20',
      lettuce: 'border-2 border-lettuce bg-transparent text-cream hover:bg-lettuce/20',
    },
    ghost: {
      bun: 'bg-bun/20 text-bun hover:bg-bun/30',
      denim: 'bg-denim/20 text-denim hover:bg-denim/30',
    },
    team: {
      ketchup: 'bg-ketchup text-cream hover:bg-ketchup/90',
      mayo: 'bg-mustard text-dark ring-1 ring-dark/10 hover:bg-mustard/90',
    },
  },

  // Cards et conteneurs
  cards: {
    default: 'bg-dark/50 ring-1 ring-cream/10',
    hero: 'bg-dark/80 shadow-2xl ring-1 ring-cream/10',
    heroOverlay: 'bg-linear-to-br from-denim/20 via-transparent to-onion/20',
  },
} as const;

export type AppTheme = typeof appTheme;
