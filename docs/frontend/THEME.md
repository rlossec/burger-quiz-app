# Thème Burger Quiz

Documentation complète du système de design de l'application Burger Quiz.

## La métaphore burger

L'interface reprend visuellement la structure d'un burger :

```
┌─────────────────────────────────────────────┐
│            HEADER  (chapeau)                │  bg: patty/90 + backdrop-blur
├═════════════════════════════════════════════╡  ← Séparateur LETTUCE 🥬
│              CONTENU (main)                 │  bg: darkAlt + blobs animés
├─────────────────────────────────────────────╡  ← Séparateur ONION  🧅
│            FOOTER  (pain du bas)            │  bg: patty/90 + backdrop-blur
└─────────────────────────────────────────────┘
```

- **Header/Footer** : Semi-transparents avec `backdrop-blur` pour voir le fond animé
- **Séparateur lettuce** : Barre verte lumineuse sous le header (la salade)
- **Séparateur onion** : Barre violette lumineuse au-dessus du footer (l'oignon)

## Architecture des fichiers

```
frontend/src/
├── theme/                        # Thème visuel partagé
│   ├── colors.ts                 # Palette OKLCH brute (styles inline)
│   ├── fonts.ts                  # Définition des polices
│   ├── tailwind.ts               # Classes Tailwind pré-composées (appTheme)
│   ├── animations.css            # Keyframes CSS partagées
│   ├── components/
│   │   ├── BackgroundEffects.tsx # Blobs, particules, grain overlay
│   │   └── index.ts
│   └── index.ts                  # Export centralisé (colors, fonts, appTheme, effets)
│
├── App.css                       # Variables CSS racine (--ketchup, etc.)
│
└── components/layout/
    ├── AuthLayout.tsx            # Layout pages publiques (login, register)
    ├── Layout.tsx                # Layout pages protégées
    ├── Header.tsx                # En-tête avec barre lettuce
    └── Footer.tsx                # Pied de page avec barre onion
```

### Usage

```tsx
// Valeurs OKLCH brutes (styles inline) + composants d'arrière-plan
import { colors, ThemeBackground } from '@/theme';
<div style={{ background: colors.patty }}>

// Classes Tailwind pré-composées (typography, buttons, text, etc.)
import { appTheme } from '@/theme';
const { typography, buttons, text } = appTheme;
<h1 className={cn(typography.h1, text.primary)}>

// Composants de fond
<ThemeBackground />  // Blobs + particules + grain
```

## Polices

| Usage                  | Police  | Poids         |
| ---------------------- | ------- | ------------- |
| Titres (h1, h2, logo)  | Syne    | 700, 800, 900 |
| Corps, boutons, inputs | DM Sans | 400, 500, 600 |

Import dans `index.html` :

```html
<link
  href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap"
  rel="stylesheet"
/>
```

## Palette de couleurs

### Couleurs principales

| Nom     | Variable CSS | OKLCH                  | Hex approx. | Usage                        |
| ------- | ------------ | ---------------------- | ----------- | ---------------------------- |
| Ketchup | `--ketchup`  | `oklch(0.5 0.18 25)`   | #B73229     | Équipe Ketchup, destructive  |
| Mustard | `--mustard`  | `oklch(0.85 0.17 90)`  | #F7C438     | Équipe Mayo, accents jaunes  |
| Denim   | `--denim`    | `oklch(0.6 0.1 260)`   | #6B7DB3     | Primary, liens actifs        |
| Onion   | `--onion`    | `oklch(0.48 0.12 340)` | #8B4A6B     | Secondary, séparateur footer |
| Lettuce | `--lettuce`  | `oklch(0.58 0.14 135)` | #5B8C3E     | Success, séparateur header   |
| Bun     | `--bun`      | `oklch(0.72 0.14 60)`  | #E59752     | Logo, titres, accents chauds |
| Patty   | `--patty`    | `oklch(0.35 0.06 45)`  | #5C3D2E     | Header/footer backgrounds    |
| Dark    | `--dark`     | `oklch(0.15 0.01 50)`  | #0E0C0B     | Fond principal               |
| DarkAlt | -            | `oklch(0.12 0.01 50)`  | #0A0908     | Fond pages (plus sombre)     |
| Cream   | `--cream`    | `oklch(0.95 0.015 85)` | #F2EBE1     | Texte principal              |

### Opacités standards

```
/10  → backgrounds très subtils
/20  → hover léger, ghost buttons
/30  → états actifs
/50  → borders, textes tertiaires
/60  → textes muted
/70  → textes inactifs
/80  → gradients, textes secondaires
/90  → hover buttons
```

## Breakpoints

Valeurs Tailwind par défaut :

| Breakpoint | Largeur | Usage                |
| ---------- | ------- | -------------------- |
| `sm`       | 640px   | Mobiles larges       |
| `md`       | 768px   | Tablettes            |
| `lg`       | 1024px  | Desktop, nav centrée |
| `xl`       | 1280px  | Grands écrans        |
| `2xl`      | 1536px  | Très grands écrans   |

## Typography

Classes responsive pour les titres et textes :

```typescript
appTheme.typography = {
  h1: "text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black tracking-tight",
  h2: "text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight",
  h3: "text-xl sm:text-2xl font-bold",
  h4: "text-lg sm:text-xl font-semibold",
  body: "text-base",
  bodyLarge: "text-lg md:text-xl",
  small: "text-sm",
  xs: "text-xs",
};
```

### Usage

```tsx
<h1 className={cn(typography.h1, text.primary)}>Titre</h1>
<p className={cn(typography.bodyLarge, text.secondary)}>Description</p>
```

## Spacing

Classes responsive pour les espacements :

```typescript
appTheme.spacing = {
  container: {
    padding: "px-4 sm:px-6 lg:px-8",
    maxWidth: "max-w-7xl",
  },
  section: {
    padding: "p-4 sm:p-6 md:p-8",
    paddingY: "py-8 md:py-12 lg:py-16",
    gap: "gap-6 md:gap-8 lg:gap-12",
  },
  card: {
    padding: "p-4 sm:p-6",
    gap: "gap-4 sm:gap-6",
  },
};
```

## Couleurs de texte

```typescript
appTheme.text = {
  primary: "text-cream", // Texte principal
  secondary: "text-cream/80", // Texte secondaire
  muted: "text-cream/60", // Texte atténué
  inactive: "text-cream/70", // Texte inactif
  subtle: "text-cream/50", // Texte très subtil
  accent: {
    ketchup: "text-ketchup",
    mayo: "text-mustard",
    bun: "text-bun",
    denim: "text-denim",
    onion: "text-onion",
    lettuce: "text-lettuce",
  },
};
```

## Boutons

### Primary & Secondary

```typescript
buttons.primary; // bg-denim text-cream hover:bg-denim/90
buttons.secondary; // bg-onion text-cream hover:bg-onion/90
```

### Outline

```typescript
buttons.outline.ketchup;
buttons.outline.mayo;
buttons.outline.denim;
buttons.outline.onion;
buttons.outline.lettuce;
```

### Ghost

```typescript
buttons.ghost.bun; // bg-bun/20 text-bun hover:bg-bun/30
buttons.ghost.denim; // bg-denim/20 text-denim hover:bg-denim/30
```

### Équipes

```typescript
buttons.team.ketchup; // bg-ketchup text-cream
buttons.team.mayo; // bg-mustard text-dark
```

### Usage

```tsx
import { Button } from '@/components/ui/button';
import { appTheme } from '@/config/theme';

<Button className={appTheme.buttons.primary}>Action principale</Button>
<Button className={appTheme.buttons.outline.denim}>Action secondaire</Button>
```

## Layout

### Backgrounds

```typescript
appTheme.layout = {
  headerBg: "bg-patty/90 backdrop-blur-md", // Semi-transparent
  footerBg: "bg-patty/90 backdrop-blur-md", // Semi-transparent
  mainText: "text-cream",
};
```

Le fond principal (`darkAlt` + blobs animés) est appliqué via le composant `<ThemeBackground />` dans les layouts.

### Séparateurs lumineux

```typescript
appTheme.separators = {
  header: {
    color: "bg-lettuce",
    glow: "shadow-[0_4px_12px_rgba(76,175,80,0.6),0_2px_4px_rgba(76,175,80,0.8)]",
    height: "h-1",
  },
  footer: {
    color: "bg-onion",
    glow: "shadow-[0_-4px_12px_rgba(156,39,176,0.5),0_-2px_4px_rgba(156,39,176,0.7)]",
    height: "h-1",
  },
};
```

## Effets de fond (ThemeBackground)

Le composant `<ThemeBackground />` combine trois effets :

1. **BackgroundBlobs** : 4 blobs colorés animés (ketchup, mustard, denim, lettuce)
2. **FloatingParticles** : 14 emojis burger flottants
3. **GrainOverlay** : Texture grain subtile (SVG filter)

```tsx
import { ThemeBackground } from "@/theme";

// Dans un layout
<div style={{ background: colors.darkAlt }}>
  <ThemeBackground />
  <div className="relative z-10">{/* Contenu */}</div>
</div>;
```

## Cards

```typescript
appTheme.cards = {
  default: "bg-dark/50 ring-1 ring-cream/10",
  hero: "bg-dark/80 shadow-2xl ring-1 ring-cream/10",
  heroOverlay: "bg-linear-to-br from-denim/20 via-transparent to-onion/20",
};
```

### Usage

```tsx
<section className={cn("rounded-2xl", spacing.card.padding, cards.default)}>
  <h2 className={cn(typography.h3, text.primary)}>Titre</h2>
  {/* contenu */}
</section>
```

## Navigation

```typescript
appTheme.nav = {
  active: "bg-denim/30 text-cream shadow-sm",
  inactive: "text-cream/70",
  hover: "hover:bg-cream/10 hover:text-bun",
};
```

## Logo

```typescript
appTheme.logo = {
  icon: {
    bg: "bg-bun/20",
    ring: "ring-2 ring-bun/30",
  },
  burger: "text-bun",
  quiz: "text-bun/80",
};
```

## Footer

```typescript
appTheme.footer = {
  title: "text-bun",
  text: "text-cream/60",
  link: "text-cream/60 hover:text-onion",
  border: "border-cream/10",
  copyright: "text-cream/50",
};
```

## Layouts

### AuthLayout (pages publiques)

Pour les pages d'authentification (login, register, etc.) :

- Fond `darkAlt` avec effets animés
- Pas de Header/Footer
- Layout deux colonnes sur desktop (artwork + formulaire)
- Logo mobile centré

### Layout (pages protégées)

Pour les pages de l'application :

- Fond `darkAlt` avec effets animés
- Header semi-transparent avec barre lettuce
- Footer semi-transparent avec barre onion
- Container responsive pour le contenu

## Mode sombre

Le thème est optimisé pour le mode sombre (`defaultTheme="dark"`). Les variables CSS dans `.dark` ajustent automatiquement les couleurs pour une meilleure lisibilité.

## Page de test

Une page de test du design system est disponible à `/drafts`. Elle affiche :

- Palette de couleurs
- Tous les styles de boutons
- Échelle typographique
- Couleurs de texte
