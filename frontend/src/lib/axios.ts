import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios';

// ─── Constantes ────────────────────────────────────────────────────────────────

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

const TOKEN_KEYS = {
  access: 'access_token',
  refresh: 'refresh_token',
} as const;

// ─── Helpers localStorage ──────────────────────────────────────────────────────

export const tokenStorage = {
  getAccess: () => localStorage.getItem(TOKEN_KEYS.access),
  getRefresh: () => localStorage.getItem(TOKEN_KEYS.refresh),
  setTokens: (access: string, refresh: string) => {
    localStorage.setItem(TOKEN_KEYS.access, access);
    localStorage.setItem(TOKEN_KEYS.refresh, refresh);
  },
  setAccess: (access: string) => {
    localStorage.setItem(TOKEN_KEYS.access, access);
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEYS.access);
    localStorage.removeItem(TOKEN_KEYS.refresh);
  },
};

import { isPublicUrl } from './publicUrls';

// ─── Instance principale ───────────────────────────────────────────────────────

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
});

// ─── Interceptor REQUEST : injecte le token JWT dans chaque requête ────────────

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (!isPublicUrl(config.url, config.method)) {
      const token = tokenStorage.getAccess();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ─── File d'attente pendant le refresh ────────────────────────────────────────

type FailedRequest = {
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
};

let isRefreshing = false;
let failedQueue: FailedRequest[] = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((req) => {
    if (token) req.resolve(token);
    else req.reject(error);
  });
  failedQueue = [];
};

// ─── Interceptor RESPONSE : refresh automatique si 401 ────────────────────────

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    if (
      error.response?.status !== 401 ||
      isPublicUrl(originalRequest?.url, originalRequest?.method) ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    // Si un refresh est déjà en cours → on met en file d'attente
    if (isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      })
        .then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return apiClient(originalRequest);
        })
        .catch(Promise.reject.bind(Promise));
    }

    // Lancement du refresh
    originalRequest._retry = true;
    isRefreshing = true;

    const refreshToken = tokenStorage.getRefresh();

    if (!refreshToken) {
      tokenStorage.clear();
      processQueue(error, null);
      isRefreshing = false;
      // Redirection vers login — adapte selon ton router
      window.location.href = '/auth/login';
      return Promise.reject(error);
    }

    try {
      // Endpoint Djoser + SimpleJWT
      const { data } = await axios.post(`${API_URL}/auth/jwt/refresh/`, {
        refresh: refreshToken,
      });

      const newAccess: string = data.access;
      tokenStorage.setAccess(newAccess);
      apiClient.defaults.headers.common.Authorization = `Bearer ${newAccess}`;

      processQueue(null, newAccess);
      originalRequest.headers.Authorization = `Bearer ${newAccess}`;
      return apiClient(originalRequest);
    } catch (refreshError) {
      tokenStorage.clear();
      processQueue(refreshError, null);
      window.location.href = '/auth/login';
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);
