# Fichiers d'environnement par service

Copiez chaque fichier `.example` en supprimant le suffixe pour créer les fichiers actifs :

```
cp db.env.example db.env
cp backend.env.example backend.env
cp pgadmin.env.example pgadmin.env
```

Les fichiers `*.env` sont ignorés par git (sauf les `.example`).

## Backend (Django)

- **DJANGO_SUPERUSER_USERNAME** / **DJANGO_SUPERUSER_EMAIL** / **DJANGO_SUPERUSER_PASSWORD** : si définies, un superuser est créé automatiquement au démarrage du container (sauf s'il existe déjà). Connexion admin avec username et mot de passe.
