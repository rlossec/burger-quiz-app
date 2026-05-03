/**
 * Constantes des endpoints API — Auth et Users.
 * Base URL configurée dans lib/axios via VITE_API_URL
 */

export const AUTH_ENDPOINTS = {
  auth: {
    login: '/auth/jwt/create/',
    refresh: '/auth/jwt/refresh/',
    verify: '/auth/jwt/verify/',
  },

  users: {
    list: '/auth/users/',
    register: '/auth/users/',
    me: '/auth/users/me/',
    detail: (id: number | string) => `/auth/users/${id}/`,
    update: (id: number | string) => `/auth/users/${id}/`,
    delete: (id: number | string) => `/auth/users/${id}/`,
    activation: '/auth/users/activation/',
    resendActivation: '/auth/users/resend_activation/',
    resetPassword: '/auth/users/reset_password/',
    resetPasswordConfirm: '/auth/users/reset_password_confirm/',
    resetUsername: '/auth/users/reset_username/',
    resetUsernameConfirm: '/auth/users/reset_username_confirm/',
    setPassword: '/auth/users/set_password/',
  },
} as const;
