# Thème Burger Quiz

Documentation complète du système de design de l'application Burger Quiz.

## Architecture

Le thème est centralisé dans `frontend/src/config/theme.ts` et expose l'objet `appTheme`.

```typescript
import { appTheme } from '@/config/theme';

const { typography, buttons, text } = appTheme;
```

Les couleurs de base sont définies dans `frontend/src/App.css` via des variables CSS OKLCH.

## Palette de couleurs

### Couleurs principales

| Nom       | Variable CSS | Hex approx. | Usage                          |
|-----------|--------------|-------------|--------------------------------|
| Ketchup   | `--ketchup`  | #B73229     | Équipe Ketchup, destructive    |
| Mayo      | `--mustard`  | #F7C438     | Équipe Mayo, accents jaunes    |
| Denim     | `--denim`    | #6B7DB3     | Primary, liens actifs          |
| Onion     | `--onion`    | #8B4A6B     | Secondary, séparateur footer   |
| Lettuce   | `--lettuce`  | #5B8C3E     | Success, séparateur header     |
| Bun       | `--bun`      | #E59752     | Logo, titres, accents chauds   |
| Patty     | `--patty`    | #5C3D2E     | Header/footer backgrounds      |
| Dark      | `--dark`     | #0E0C0B     | Fond principal                 |
| Cream     | `--cream`    | #F2EBE1     | Texte principal                |

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

Valeurs Tailwind par défaut, référencées dans `appTheme.breakpoints` :

| Breakpoint | Largeur | Usage                    |
|------------|---------|--------------------------|
| `sm`       | 640px   | Mobiles larges           |
| `md`       | 768px   | Tablettes                |
| `lg`       | 1024px  | Desktop, nav centrée     |
| `xl`       | 1280px  | Grands écrans            |
| `2xl`      | 1536px  | Très grands écrans       |

## Typography

Classes responsive pour les titres et textes :

```typescript
appTheme.typography = {
  h1: 'text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black tracking-tight',
  h2: 'text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight',
  h3: 'text-xl sm:text-2xl font-bold',
  h4: 'text-lg sm:text-xl font-semibold',
  body: 'text-base',
  bodyLarge: 'text-lg md:text-xl',
  small: 'text-sm',
  xs: 'text-xs',
}
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
}
```

## Couleurs de texte

```typescript
appTheme.text = {
  primary: 'text-cream',           // Texte principal
  secondary: 'text-cream/80',      // Texte secondaire
  muted: 'text-cream/60',          // Texte atténué
  inactive: 'text-cream/70',       // Texte inactif
  subtle: 'text-cream/50',         // Texte très subtil
  accent: {
    ketchup: 'text-ketchup',
    mayo: 'text-mustard',
    bun: 'text-bun',
    denim: 'text-denim',
    onion: 'text-onion',
    lettuce: 'text-lettuce',
  },
}
```

## Boutons

### Primary & Secondary

```typescript
buttons.primary   // bg-denim text-cream hover:bg-denim/90
buttons.secondary // bg-onion text-cream hover:bg-onion/90
```

### Outline

```typescript
buttons.outline.ketchup
buttons.outline.mayo
buttons.outline.denim
buttons.outline.onion
buttons.outline.lettuce
```

### Ghost

```typescript
buttons.ghost.bun   // bg-bun/20 text-bun hover:bg-bun/30
buttons.ghost.denim // bg-denim/20 text-denim hover:bg-denim/30
```

### Équipes

```typescript
buttons.team.ketchup // bg-ketchup text-cream
buttons.team.mayo    // bg-mustard text-dark
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
  headerBg: 'bg-linear-to-b from-patty via-patty/80 to-dark',
  footerBg: 'bg-linear-to-t from-patty via-patty/80 to-dark',
  mainBg: 'bg-linear-to-b from-dark via-onion/10 to-dark',
  mainText: 'text-cream',
}
```

### Séparateurs lumineux

```typescript
appTheme.separators = {
  header: {
    color: 'bg-lettuce',
    glow: 'shadow-[0_4px_12px_rgba(76,175,80,0.6),...]',
    height: 'h-1',
  },
  footer: {
    color: 'bg-onion',
    glow: 'shadow-[0_-4px_12px_rgba(156,39,176,0.5),...]',
    height: 'h-1',
  },
}
```

## Cards

```typescript
appTheme.cards = {
  default: 'bg-dark/50 ring-1 ring-cream/10',
  hero: 'bg-dark/80 shadow-2xl ring-1 ring-cream/10',
  heroOverlay: 'bg-linear-to-br from-denim/20 via-transparent to-onion/20',
}
```

### Usage

```tsx
<section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
  <h2 className={cn(typography.h3, text.primary)}>Titre</h2>
  {/* contenu */}
</section>
```

## Navigation

```typescript
appTheme.nav = {
  active: 'bg-denim/30 text-cream shadow-sm',
  inactive: 'text-cream/70',
  hover: 'hover:bg-cream/10 hover:text-bun',
}
```

## Logo

```typescript
appTheme.logo = {
  icon: {
    bg: 'bg-bun/20',
    ring: 'ring-2 ring-bun/30',
  },
  burger: 'text-bun',
  quiz: 'text-bun/80',
}
```

## Footer

```typescript
appTheme.footer = {
  title: 'text-bun',
  text: 'text-cream/60',
  link: 'text-cream/60 hover:text-onion',
  border: 'border-cream/10',
  copyright: 'text-cream/50',
}
```

## Mode sombre

Le thème est optimisé pour le mode sombre (`defaultTheme="dark"`). Les variables CSS dans `.dark` ajustent automatiquement les couleurs pour une meilleure lisibilité.

## Page de test

Une page de test du design system est disponible à `/drafts` (lien temporaire dans la navigation). Elle affiche :

- Palette de couleurs
- Tous les styles de boutons
- Échelle typographique
- Couleurs de texte

## Fichiers clés

```
frontend/src/
├── config/
│   └── theme.ts          # Configuration centralisée du thème
├── App.css               # Variables CSS (couleurs OKLCH)
├── providers/
│   └── theme.tsx         # ThemeProvider (next-themes)
└── components/layout/
    ├── Header.tsx        # Header responsive
    ├── Footer.tsx        # Footer responsive
    ├── Nav.tsx           # Navigation
    ├── Container.tsx     # Container responsive
    └── Layout.tsx        # Layout principal
```
