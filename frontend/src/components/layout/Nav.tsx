import { NavLink } from 'react-router-dom';
import { Home, HelpCircle, Play, Palette } from 'lucide-react';
import { cn } from '@/lib/utils';
import { appTheme } from '@/config/theme';

interface NavProps {
  className?: string;
  onNavigate?: () => void;
}

const navItems = [
  { to: '/', label: 'Accueil', icon: Home },
  { to: '/quiz', label: 'Mes Quiz', icon: HelpCircle },
  { to: '/play', label: 'Jouer', icon: Play },
  { to: '/drafts', label: 'Drafts', icon: Palette, temp: true },
];

export function Nav({ className, onNavigate }: NavProps) {
  const { nav } = appTheme;

  return (
    <nav className={cn('flex items-center gap-1', className)}>
      {navItems.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          onClick={onNavigate}
          className={({ isActive }) =>
            cn(
              'group flex items-center gap-2 rounded-lg px-4 py-2.5 font-semibold transition-all',
              isActive ? nav.active : cn(nav.inactive, nav.hover),
              'temp' in item && item.temp && 'border border-dashed border-onion/50'
            )
          }
        >
          <item.icon className="h-4 w-4 transition-transform group-hover:scale-110" />
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
