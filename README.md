# Burger Quiz 🍔

Application web pour animer des soirées Burger Quiz : préparation des manches, diffusion des questions et gestion des scores des équipes.

## Stack

| Composant | Techno |
|-----------|--------|
| Backend | Django 6, Django REST Framework, Python 3.12 |
| Frontend | React, TypeScript, Vite |
| Base de données | PostgreSQL 18 |
| Infra | Docker Compose |

## Démarrage rapide

**Prérequis :** Docker & Docker Compose

```bash
# 1. Configurer l'environnement
cp env/db.env.example env/db.env
cp env/backend.env.example env/backend.env
cp env/pgadmin.env.example env/pgadmin.env

# 2. Lancer l'application
docker compose up -d

# 3. Appliquer les migrations (première fois)
docker compose exec backend python manage.py migrate

# 4. Créer un superutilisateur (optionnel)
docker compose exec backend python manage.py createsuperuser

# Avec pgAdmin (optionnel)
docker compose --profile tools up -d
```

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Django Admin | http://localhost:8000/admin/ |
| pgAdmin | http://localhost:5050 |

## Structure

```
burger-quiz-app/
├── backend/              # Django + DRF
│   ├── accounts/         # App utilisateurs (CustomUser)
│   ├── config/           # Settings, URLs
│   ├── manage.py
│   └── Dockerfile
├── frontend/             # React + Vite
│   ├── src/
│   └── Dockerfile
├── env/                  # Variables par service (db, backend, pgadmin)
└── docker-compose.yml
```

## Variables d'environnement

- **`env/`** : fichiers par service — voir `env/README.md`
