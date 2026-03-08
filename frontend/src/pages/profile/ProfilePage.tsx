import { useState, useRef } from 'react';
import { User, Mail, Edit, Lock, Camera, AlertTriangle, LogOut } from 'lucide-react';
import { cn } from '@/lib/utils';

import { appTheme, colors } from '@/theme';
import { useAuthStore, type AuthState } from '@/stores';

import { apiClient, tokenStorage } from '@/lib/axios';
import { AUTH_ENDPOINTS } from '@/features/auth/api';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

type ModalType = 'avatar' | 'email' | 'username' | 'password' | null;

export function ProfilePage() {
  const { cards, text, typography, spacing } = appTheme;
  const user = useAuthStore((state: AuthState) => state.user);
  const updateUser = useAuthStore((state: AuthState) => state.updateUser);
  const logout = useAuthStore((state: AuthState) => state.logout);

  // États d'édition inline
  const [editingField, setEditingField] = useState<'first_name' | 'last_name' | null>(null);
  const [firstName, setFirstName] = useState(user?.first_name ?? '');
  const [lastName, setLastName] = useState(user?.last_name ?? '');

  // État des modales
  const [activeModal, setActiveModal] = useState<ModalType>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // États des formulaires modales
  const [newEmail, setNewEmail] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!user) {
    return (
      <div className="flex items-center justify-center py-12">
        <p className={text.muted}>Chargement...</p>
      </div>
    );
  }

  const displayName =
    user.first_name || user.last_name
      ? `${user.first_name} ${user.last_name}`.trim()
      : user.username;

  const initials = displayName
    .split(' ')
    .map((n: string) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  // ─── Handlers ─────────────────────────────────────────────────────────────────

  const resetModalState = () => {
    setError(null);
    setNewEmail('');
    setNewUsername('');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setAvatarFile(null);
    setAvatarPreview(null);
  };

  const openModal = (type: ModalType) => {
    resetModalState();
    if (type === 'email') setNewEmail(user.email);
    if (type === 'username') setNewUsername(user.username);
    setActiveModal(type);
  };

  const closeModal = () => {
    setActiveModal(null);
    resetModalState();
  };

  const handleLogoutAfterChange = () => {
    tokenStorage.clear();
    logout();
    window.location.href = '/auth/login';
  };

  // Sauvegarde nom/prénom inline
  const handleSaveName = async (field: 'first_name' | 'last_name') => {
    setIsLoading(true);
    try {
      const value = field === 'first_name' ? firstName : lastName;
      await apiClient.patch(AUTH_ENDPOINTS.users.me, { [field]: value });
      updateUser({ [field]: value });
      setEditingField(null);
    } catch {
      setError('Erreur lors de la mise à jour');
    } finally {
      setIsLoading(false);
    }
  };

  // Sauvegarde avatar
  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAvatarFile(file);
      const reader = new FileReader();
      reader.onload = () => setAvatarPreview(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleSaveAvatar = async () => {
    if (!avatarFile) return;
    setIsLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('avatar', avatarFile);
      const response = await apiClient.patch(AUTH_ENDPOINTS.users.me, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      updateUser({ avatar: response.data.avatar });
      closeModal();
    } catch {
      setError("Erreur lors de l'upload de l'avatar");
    } finally {
      setIsLoading(false);
    }
  };

  // Changement email
  const handleChangeEmail = async () => {
    if (newEmail === user.email) {
      closeModal();
      return;
    }
    if (!currentPassword) {
      setError('Veuillez entrer votre mot de passe actuel');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.patch(AUTH_ENDPOINTS.users.me, {
        email: newEmail,
        current_password: currentPassword,
      });
      handleLogoutAfterChange();
    } catch {
      setError("Mot de passe incorrect ou erreur lors du changement d'email");
      setIsLoading(false);
    }
  };

  // Changement username
  const handleChangeUsername = async () => {
    if (newUsername === user.username) {
      closeModal();
      return;
    }
    if (!currentPassword) {
      setError('Veuillez entrer votre mot de passe actuel');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.patch(AUTH_ENDPOINTS.users.me, {
        username: newUsername,
        current_password: currentPassword,
      });
      handleLogoutAfterChange();
    } catch {
      setError("Mot de passe incorrect ou erreur lors du changement de nom d'utilisateur");
      setIsLoading(false);
    }
  };

  // Changement mot de passe
  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      await apiClient.post(AUTH_ENDPOINTS.users.setPassword, {
        current_password: currentPassword,
        new_password: newPassword,
        re_new_password: confirmPassword,
      });
      handleLogoutAfterChange();
    } catch {
      setError('Mot de passe actuel incorrect ou nouveau mot de passe invalide');
      setIsLoading(false);
    }
  };

  // ─── Render ───────────────────────────────────────────────────────────────────

  return (
    <div className={cn('space-y-8', spacing.section.gap)}>
      {/* Header avec avatar */}
      <section
        className={cn(
          'relative overflow-hidden rounded-3xl',
          spacing.section.padding,
          cards.hero,
          text.primary
        )}
      >
        <div className={cn('absolute inset-0', cards.heroOverlay)} />

        <div className="relative z-10 flex flex-col items-center gap-6 sm:flex-row sm:items-start sm:gap-8">
          {/* Avatar */}
          <div className="relative">
            {user.avatar ? (
              <img
                src={user.avatar}
                alt={displayName}
                className="h-28 w-28 rounded-full object-cover ring-4 ring-cream/20 sm:h-32 sm:w-32"
              />
            ) : (
              <div
                className="flex h-28 w-28 items-center justify-center rounded-full text-3xl font-bold ring-4 ring-cream/20 sm:h-32 sm:w-32 sm:text-4xl"
                style={{ background: colors.denim, color: colors.cream }}
              >
                {initials}
              </div>
            )}
            <button
              onClick={() => openModal('avatar')}
              className="absolute -bottom-1 -right-1 flex h-10 w-10 items-center justify-center rounded-full bg-bun text-dark transition-transform hover:scale-110"
              title="Modifier la photo"
            >
              <Camera className="h-5 w-5" />
            </button>
          </div>

          {/* Infos */}
          <div className="flex-1 text-center sm:text-left">
            <h1 className={cn(typography.h2, 'mb-2')}>{displayName}</h1>
            <p
              className={cn(
                text.secondary,
                'flex items-center justify-center gap-2 sm:justify-start'
              )}
            >
              <span className="text-bun">@{user.username}</span>
            </p>
          </div>
        </div>
      </section>

      {/* Informations du compte */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h4, text.primary, 'mb-6')}>Informations du compte</h2>

        <div className="space-y-4">
          {/* Email */}
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-denim/20">
                <Mail className="h-5 w-5 text-denim" />
              </div>
              <div>
                <p className={cn(text.muted, 'text-sm')}>Email</p>
                <p className={text.primary}>{user.email}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => openModal('email')}
              className="bg-primary/20 text-primary hover:bg-primary/30"
            >
              Modifier
            </Button>
          </div>

          {/* Nom d'utilisateur */}
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-onion/20">
                <User className="h-5 w-5 text-onion" />
              </div>
              <div>
                <p className={cn(text.muted, 'text-sm')}>Nom d'utilisateur</p>
                <p className={text.primary}>{user.username}</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => openModal('username')}
              className="bg-primary/20 text-primary hover:bg-primary/30"
            >
              Modifier
            </Button>
          </div>

          {/* Prénom */}
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-lettuce/20">
                <Edit className="h-5 w-5 text-lettuce" />
              </div>
              <div className="flex-1">
                <p className={cn(text.muted, 'text-sm')}>Prénom</p>
                {editingField === 'first_name' ? (
                  <Input
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="mt-1 h-8 bg-dark/50 border-cream/20"
                    autoFocus
                  />
                ) : (
                  <p className={text.primary}>{user.first_name || '—'}</p>
                )}
              </div>
            </div>
            {editingField === 'first_name' ? (
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setFirstName(user.first_name ?? '');
                    setEditingField(null);
                  }}
                  className="text-cream/60"
                >
                  Annuler
                </Button>
                <Button
                  size="sm"
                  onClick={() => handleSaveName('first_name')}
                  disabled={isLoading}
                  className=""
                >
                  Enregistrer
                </Button>
              </div>
            ) : (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setFirstName(user.first_name ?? '');
                  setEditingField('first_name');
                }}
                className="bg-primary/20 text-primary hover:bg-primary/30"
              >
                Modifier
              </Button>
            )}
          </div>

          {/* Nom */}
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-lettuce/20">
                <Edit className="h-5 w-5 text-lettuce" />
              </div>
              <div className="flex-1">
                <p className={cn(text.muted, 'text-sm')}>Nom</p>
                {editingField === 'last_name' ? (
                  <Input
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="mt-1 h-8 bg-dark/50 border-cream/20"
                    autoFocus
                  />
                ) : (
                  <p className={text.primary}>{user.last_name || '—'}</p>
                )}
              </div>
            </div>
            {editingField === 'last_name' ? (
              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setLastName(user.last_name ?? '');
                    setEditingField(null);
                  }}
                  className="text-cream/60"
                >
                  Annuler
                </Button>
                <Button
                  size="sm"
                  onClick={() => handleSaveName('last_name')}
                  disabled={isLoading}
                  className=""
                >
                  Enregistrer
                </Button>
              </div>
            ) : (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setLastName(user.last_name ?? '');
                  setEditingField('last_name');
                }}
                className="bg-primary/20 text-primary hover:bg-primary/30"
              >
                Modifier
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Sécurité */}
      <section className={cn('rounded-2xl', spacing.card.padding, cards.default)}>
        <h2 className={cn(typography.h4, text.primary, 'mb-6')}>Sécurité</h2>

        <div className="space-y-4">
          {/* Mot de passe */}
          <div className="flex items-center justify-between rounded-xl bg-cream/5 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-ketchup/20">
                <Lock className="h-5 w-5 text-ketchup" />
              </div>
              <div>
                <p className={cn(text.muted, 'text-sm')}>Mot de passe</p>
                <p className={text.primary}>••••••••</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => openModal('password')}
              className="bg-primary/20 text-primary hover:bg-primary/30"
            >
              Modifier
            </Button>
          </div>
        </div>
      </section>

      {/* ─── Modales ───────────────────────────────────────────────────────────── */}

      {/* Modale Avatar */}
      <Dialog open={activeModal === 'avatar'} onOpenChange={(open) => !open && closeModal()}>
        <DialogContent className="bg-dark border-cream/10 text-cream">
          <DialogHeader>
            <DialogTitle>Modifier la photo de profil</DialogTitle>
            <DialogDescription className="text-cream/60">
              Sélectionnez une nouvelle image pour votre avatar.
            </DialogDescription>
          </DialogHeader>

          <div className="flex flex-col items-center gap-4 py-4">
            {avatarPreview ? (
              <img
                src={avatarPreview}
                alt="Aperçu"
                className="h-32 w-32 rounded-full object-cover ring-4 ring-cream/20"
              />
            ) : user.avatar ? (
              <img
                src={user.avatar}
                alt={displayName}
                className="h-32 w-32 rounded-full object-cover ring-4 ring-cream/20"
              />
            ) : (
              <div
                className="flex h-32 w-32 items-center justify-center rounded-full text-4xl font-bold ring-4 ring-cream/20"
                style={{ background: colors.denim, color: colors.cream }}
              >
                {initials}
              </div>
            )}

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleAvatarChange}
              className="hidden"
            />
            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
              className="border-cream/20 text-cream hover:bg-cream/10"
            >
              <Camera className="mr-2 h-4 w-4" />
              Choisir une image
            </Button>
          </div>

          {error && <p className="text-sm text-ketchup text-center">{error}</p>}

          <DialogFooter>
            <Button variant="ghost" onClick={closeModal} className="text-cream/60">
              Annuler
            </Button>
            <Button onClick={handleSaveAvatar} disabled={!avatarFile || isLoading} className="">
              {isLoading ? 'Envoi...' : 'Enregistrer'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modale Email */}
      <Dialog open={activeModal === 'email'} onOpenChange={(open) => !open && closeModal()}>
        <DialogContent className="bg-dark border-cream/10 text-cream">
          <DialogHeader>
            <DialogTitle>Modifier l'email</DialogTitle>
            <DialogDescription className="text-cream/60">
              Entrez votre nouvelle adresse email.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="new-email" className="text-cream/80">
                Nouvel email
              </Label>
              <Input
                id="new-email"
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email-password" className="text-cream/80">
                Mot de passe actuel
              </Label>
              <Input
                id="email-password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Confirmez votre identité"
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            {/* Avertissement */}
            <div className="flex items-start gap-3 rounded-lg bg-mustard/10 p-3 text-sm">
              <AlertTriangle className="h-5 w-5 shrink-0 text-mustard" />
              <div className="text-cream/80">
                <p className="font-medium text-mustard">Attention</p>
                <p>
                  Un email d'activation sera envoyé à cette nouvelle adresse. Vous serez déconnecté
                  et devrez activer votre compte avant de pouvoir vous reconnecter.
                </p>
              </div>
            </div>
          </div>

          {error && <p className="text-sm text-ketchup text-center">{error}</p>}

          <DialogFooter>
            <Button variant="ghost" onClick={closeModal} className="text-cream/60">
              Annuler
            </Button>
            <Button
              onClick={handleChangeEmail}
              disabled={!newEmail || newEmail === user.email || !currentPassword || isLoading}
              className=""
            >
              <LogOut className="mr-2 h-4 w-4" />
              {isLoading ? 'Modification...' : 'Confirmer et déconnecter'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modale Username */}
      <Dialog open={activeModal === 'username'} onOpenChange={(open) => !open && closeModal()}>
        <DialogContent className="bg-dark border-cream/10 text-cream">
          <DialogHeader>
            <DialogTitle>Modifier le nom d'utilisateur</DialogTitle>
            <DialogDescription className="text-cream/60">
              Entrez votre nouveau nom d'utilisateur.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="new-username" className="text-cream/80">
                Nouveau nom d'utilisateur
              </Label>
              <Input
                id="new-username"
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="username-password" className="text-cream/80">
                Mot de passe actuel
              </Label>
              <Input
                id="username-password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Confirmez votre identité"
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            {/* Avertissement */}
            <div className="flex items-start gap-3 rounded-lg bg-mustard/10 p-3 text-sm">
              <AlertTriangle className="h-5 w-5 shrink-0 text-mustard" />
              <div className="text-cream/80">
                <p className="font-medium text-mustard">Attention</p>
                <p>Pour des raisons de sécurité, vous serez déconnecté après cette modification.</p>
              </div>
            </div>
          </div>

          {error && <p className="text-sm text-ketchup text-center">{error}</p>}

          <DialogFooter>
            <Button variant="ghost" onClick={closeModal} className="text-cream/60">
              Annuler
            </Button>
            <Button
              onClick={handleChangeUsername}
              disabled={
                !newUsername || newUsername === user.username || !currentPassword || isLoading
              }
              className=""
            >
              <LogOut className="mr-2 h-4 w-4" />
              {isLoading ? 'Modification...' : 'Confirmer et déconnecter'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Modale Mot de passe */}
      <Dialog open={activeModal === 'password'} onOpenChange={(open) => !open && closeModal()}>
        <DialogContent className="bg-dark border-cream/10 text-cream">
          <DialogHeader>
            <DialogTitle>Modifier le mot de passe</DialogTitle>
            <DialogDescription className="text-cream/60">
              Entrez votre mot de passe actuel puis votre nouveau mot de passe.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="current-password" className="text-cream/80">
                Mot de passe actuel
              </Label>
              <Input
                id="current-password"
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="new-password" className="text-cream/80">
                Nouveau mot de passe
              </Label>
              <Input
                id="new-password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirm-password" className="text-cream/80">
                Confirmer le nouveau mot de passe
              </Label>
              <Input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="bg-dark/50 border-cream/20 text-cream"
              />
            </div>

            {/* Avertissement */}
            <div className="flex items-start gap-3 rounded-lg bg-mustard/10 p-3 text-sm">
              <AlertTriangle className="h-5 w-5 shrink-0 text-mustard" />
              <div className="text-cream/80">
                <p className="font-medium text-mustard">Attention</p>
                <p>Vous serez déconnecté après le changement de mot de passe.</p>
              </div>
            </div>
          </div>

          {error && <p className="text-sm text-ketchup text-center">{error}</p>}

          <DialogFooter>
            <Button variant="ghost" onClick={closeModal} className="text-cream/60">
              Annuler
            </Button>
            <Button
              onClick={handleChangePassword}
              disabled={!currentPassword || !newPassword || !confirmPassword || isLoading}
              className=""
            >
              <LogOut className="mr-2 h-4 w-4" />
              {isLoading ? 'Modification...' : 'Confirmer et déconnecter'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
