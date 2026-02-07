# Burger Quiz 🍔

Application web pour animer des soirées Burger Quiz : préparation des manches, diffusion des questions et gestion des scores des équipes.

## Stack

| Composant | Techno |
|-----------|--------|
| Backend | FastAPI, Python 3.12, SQLAlchemy |
| Frontend | React, TypeScript, Vite |
| Base de données | PostgreSQL 18 |
| Infra | Docker Compose |

## Démarrage rapide

**Prérequis :** Docker & Docker Compose

```bash
# 1. Configurer l'environnement
cp .env.example .env
cp env/db.env.example env/db.env
cp env/backend.env.example env/backend.env
cp env/pgadmin.env.example env/pgadmin.env

# 2. Lancer l'application
docker compose up -d

# Avec pgAdmin (optionnel)
docker compose --profile tools up -d
```

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |

## Structure

```
BurgerQuizApp/
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── api/      # Routes
│   │   └── core/     # Config, logging
│   └── Dockerfile
├── frontend/         # React + Vite
│   ├── src/
│   └── Dockerfile
├── env/              # Variables par service (db, backend, pgadmin)
├── docs/             # Documentation (MCD, etc.)
└── docker-compose.yml
```

## Variables d'environnement

- **`env/`** : fichiers par service — voir `env/README.md`
