# Wireframes — Layout global

Réf. : [page_reference](../page_reference.md) · [README](README.md)

## Sommaire

- [Layout global](#layout-global)

---

## Layout global

### Principe

Structure commune à toutes les pages (hors Login) : navbar avec logo, liens (Burger Quiz, Questions, etc.), zone utilisateur et logout ; fil d’Ariane ou titre de page ; zone de contenu (liste, formulaire ou détail).

### Wireframe

```
+------------------------------------------------------------------+
|  [Logo] Burger Quiz    Navbar : Burger Quiz | Nuggets | ...  [User] [Logout]  |
+------------------------------------------------------------------+
|  Fil d'Ariane (optionnel)  ou  Titre de la page                  |
|  +------------------------------------------------------------+  |
|  |                    Zone de contenu                         |  |
|  |                    (liste, formulaire, détail)             |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### Appels API

Aucun appel direct pour le layout. Les pages filles utilisent le token JWT (obtenu via `POST /api/auth/jwt/create/`) dans l’en-tête `Authorization: Bearer <access>`.
