# Flux Auth

Flux d'authentification utilisateur.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                        AUTH FLOW                            │
├─────────────────────────────────────────────────────────────┤
│  Register → Email Sent → Activate → Login → Dashboard       │
│                                                             │
│  Forgot Password → Email Sent → Reset Password → Login      │
│                                                             │
│  Login → Dashboard                                          │
│  Logout → Login                                             │
└─────────────────────────────────────────────────────────────┘
```

## 1. Inscription

```
[RegisterPage]
     │
     ▼
(Saisie email, username, password, confirm)
     │
     ▼
[[POST /auth/users/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [EmailSentPage] "Vérifiez votre email"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs (email existe, password faible...)
```

### États

```typescript
// Pendant l'inscription
isLoading: true

// Après succès
redirect → /auth/email-sent
```

## 2. Activation du compte

```
[Email reçu]
     │
     ▼
(Clic sur lien /auth/activate/:uid/:token)
     │
     ▼
[ActivatePage]
     │
     ▼
[[POST /auth/users/activation/]]
     │
     ├── ✅ 204 No Content
     │        │
     │        ▼
     │   redirect → [LoginPage] + toast "Compte activé"
     │
     └── ❌ 400 Bad Request (token invalide/expiré)
              │
              ▼
         [ActivatePage] avec message erreur
         + lien vers "Renvoyer l'email"
```

---

## 3. Renvoi email d'activation

```
[ResendActivationPage]
     │
     ▼
(Saisie email)
     │
     ▼
[[POST /auth/users/resend_activation/]]
     │
     ├── ✅ 204 No Content
     │        │
     │        ▼
     │   Afficher message
     │
     └── ❌ 400 (email non trouvé ou déjà activé)
              │
              ▼
         Afficher message
```

## 4. Connexion

### Flux

```
[LoginPage]
     │
     ▼
(Saisie email, password)
     │
     ▼
[[POST /auth/jwt/create/]]
     │
     ├── ✅ 200 OK { access, refresh }
     │        │
     │        ▼
     │   <<AuthStore.login(tokens)>>
     │        │
     │        ▼
     │   [[GET /auth/users/me/]]
     │        │
     │        ▼
     │   <<AuthStore.setUser(user)>>
     │        │
     │        ▼
     │   redirect → [Dashboard] ou ?redirect=...
     │
     └── ❌ 401 Unauthorized
              │
              ▼
         Afficher erreur "Identifiants incorrects"
```

### États après login

```typescript
// AuthStore
{
  user: { id, email, username, avatar },
  tokens: { access, refresh },
  isAuthenticated: true,
  isLoading: false
}
```

## 5. Déconnexion

### Flux

```
[N'importe quelle page]
     │
     ▼
(Clic "Déconnexion")
     │
     ▼
<<AuthStore.logout()>>
     │
     ▼
localStorage.clear("auth-storage")
     │
     ▼
redirect → [HomePage] ou [LoginPage]
```

### États après logout

```typescript
// AuthStore
{
  user: null,
  tokens: null,
  isAuthenticated: false
}
```

---

## 6. Mot de passe oublié

### Flux - Demande

```
[ForgotPasswordPage]
     │
     ▼
(Saisie email)
     │
     ▼
[[POST /auth/users/reset_password/]]
     │
     ▼
[EmailSentPage] "Si ce compte existe, un email a été envoyé"
```

### Flux - Reset

```
[Email reçu]
     │
     ▼
(Clic sur lien /auth/password/reset/confirm/:uid/:token)
     │
     ▼
[ResetPasswordPage]
     │
     ▼
(Saisie new_password, re_new_password)
     │
     ▼
[[POST /auth/users/reset_password_confirm/]]
     │
     ├── ✅ 204 No Content
     │        │
     │        ▼
     │   redirect → [LoginPage] + toast "Mot de passe modifié"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreur (token expiré, password faible...)
```

## 7. Refresh Token

```
[[Requête API quelconque]]
     │
     ▼
{Response 401?}
     │
     ├── Non → Retourner response
     │
     └── Oui
          │
          ▼
     [[POST /auth/jwt/refresh/]]
          │
          ├── ✅ 200 { access }
          │        │
          │        ▼
          │   <<AuthStore.setTokens({ access, refresh })>>
          │        │
          │        ▼
          │   Rejouer la requête originale
          │
          └── ❌ 401 (refresh expiré)
                   │
                   ▼
              <<AuthStore.logout()>>
                   │
                   ▼
              redirect → [LoginPage]
```

## 8. Protection des routes

### ProtectedRoute Component

```
[Route protégée]
     │
     ▼
{isAuthenticated?}
     │
     ├── Oui → Afficher la page
     │
     └── Non
          │
          ▼
     {isLoading?}
          │
          ├── Oui → Afficher Loader
          │
          └── Non → redirect → /login?redirect={currentUrl}
```

### Implémentation

```tsx
// src/components/common/ProtectedRoute.tsx

function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuthStore();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to={`/login?redirect=${location.pathname}`} replace />;
  }

  return <Outlet />;
}
```

---
