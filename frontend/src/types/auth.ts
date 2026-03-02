/**
 * Types pour l'authentification et les utilisateurs
 */

export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  avatar: string | null;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

// ─── Requêtes ───────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  re_password: string;
}

export interface ActivationRequest {
  uid: string;
  token: string;
}

export interface ResetPasswordRequest {
  email: string;
}

export interface ResetPasswordConfirmRequest {
  uid: string;
  token: string;
  new_password: string;
  re_new_password: string;
}

export interface SetPasswordRequest {
  current_password: string;
  new_password: string;
  re_new_password: string;
}

export interface UpdateUserRequest {
  email?: string;
  first_name?: string;
  last_name?: string;
  avatar?: File | null;
}
