import { PageWrapper } from '../PageWrapper';
import { Nav } from '../Nav';

import { HeaderUserActions } from './HeaderUserActions';
import { cn } from '@/lib/utils';
import { colors } from '@/theme';

type MobileMenuPanelProps = {
  open: boolean;
  username?: string | null;
  onLogout: () => void;
  onNavigate: () => void;
};

/**
 * Panneau déroulant du menu mobile : Nav + profil + déconnexion.
 */
export function MobileMenuPanel({ open, username, onLogout, onNavigate }: MobileMenuPanelProps) {
  return (
    <div
      className={cn('overflow-hidden transition-all duration-300 md:hidden')}
      style={{
        background: `linear-gradient(to bottom, ${colors.patty}cc, ${colors.dark})`,
        maxHeight: open ? '24rem' : '0',
      }}
    >
      <PageWrapper>
        <div className="space-y-4 py-4">
          <Nav className="flex-col items-stretch gap-1" onNavigate={onNavigate} />
          <div className="border-t" style={{ borderColor: `${colors.cream}1a` }} />
          <HeaderUserActions
            username={username}
            onLogout={onLogout}
            variant="mobile"
            onNavigate={onNavigate}
          />
        </div>
      </PageWrapper>
    </div>
  );
}
