/**
 * Tokens d'authentification (JWT).
 */

/* POST /api/auth/jwt/create/ */
export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

/* POST /api/auth/jwt/refresh/ */
export interface RefreshRequest {
  refresh: string;
}

export interface RefreshResponse {
  access: string;
}

/* POST /api/auth/jwt/verify/ */
export interface VerifyRequest {
  token: string;
}

export interface VerifyResponse {
  valid: boolean;
}

/* POST /api/auth/users/ */
export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  re_password: string;
}

/* POST /api/auth/users/activation/ */
export interface ActivationRequest {
  uid: string;
  token: string;
}

/* POST /api/auth/users/resend_activation/ */
export interface ResendActivationRequest {
  email: string;
}

/* POST /api/auth/users/reset_password/ */
export interface ResetPasswordRequest {
  email: string;
}

/* POST /api/auth/users/reset_password_confirm/ */
export interface ResetPasswordConfirmRequest {
  uid: string;
  token: string;
  new_password: string;
}

/* POST /api/auth/users/reset_username/ */
export interface ResetUsernameRequest {
  email: string;
}

/* POST /api/auth/users/reset_username_confirm/ */
export interface ResetUsernameConfirmRequest {
  new_username: string;
}

/* POST /api/auth/users/set_password/ */
export interface SetPasswordRequest {
  current_password: string;
  new_password: string;
}

/* POST /api/auth/users/set_username/ */
export interface SetUsernameRequest {
  current_password: string;
  new_username: string;
}

/**
 * Utilisateur (profil /users/me).
 */

/* GET /api/auth/users/, GET /api/auth/users/{id}/, GET /api/auth/users/me/ */
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  avatar: string | null;
}

/* PATCH /api/auth/users/me/ */
export interface UserUpdateRequest {
  email?: string;
  first_name?: string;
  last_name?: string;
  avatar?: string | null;
}
