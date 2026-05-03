# Burger Quiz 🍔

Application web pour animer des soirées Burger Quiz :

- Création des manches et émissions
- Création de session de jeu
- Diffusion des questions et animations
- Gestion des scores des équipes.

## Stack

| Composant       | Techno                                       |
| --------------- | -------------------------------------------- |
| Backend         | Django 6, Django REST Framework, Python 3.12 |
| Frontend        | React, TypeScript, Vite, Tailwind CSS        |
| Base de données | PostgreSQL 18                                |
| Infra           | Docker Compose                               |

## Quick Start

**Prérequis :** Docker & Docker Compose

- **`env/`** : fichiers par service — voir fx`env/README.md`

```bash
# 1. Configurer l'environnement
cp env/db.env.example env/db.env
cp env/backend.env.example env/backend.env
cp env/pgadmin.env.example env/pgadmin.env

# 2. Lancer l'application
docker compose up -d

# 3. Migrations et superuser (automatiques au démarrage)
# Définir DJANGO_SUPERUSER_EMAIL et DJANGO_SUPERUSER_PASSWORD dans env/backend.env

# Avec pgAdmin (optionnel)
docker compose --profile tools up -d
```

On retrouver les élements de l'application :

| Service      | URL                          |
| ------------ | ---------------------------- |
| Frontend     | http://localhost:5173        |
| Backend API  | http://localhost:8000        |
| Django Admin | http://localhost:8000/admin/ |
| pgAdmin      | http://localhost:5050        |

### Fixtures

Le dossier `backend/src/fixtures` est monté dans le conteneur. Les commandes Django doivent être exécutées **dans le conteneur** :

```bash
# Charger les données
docker compose exec backend uv run python manage.py loaddata fixtures/quiz_data.json

# Exporter les données (depuis la racine du projet)
docker compose exec backend uv run python manage.py dumpdata --indent 2 quiz > backend/src/fixtures/quiz_data.json
```

→ Voir [docs/fixtures.md](docs/fixtures.md) pour plus de détails.

## Structure

```

burger-quiz-app/
├── backend/              # Django + DRF
│   ├── src/              # Code applicatif
│   │   ├── config/       # Settings, URLs
│   │   ├── accounts/     # App utilisateurs (CustomUser)
│   │   ├── quiz/         # App quiz
│   │   ├── fixtures/     # Données (monté en volume Docker)
│   │   └── manage.py
│   └── Dockerfile
├── frontend/             # React + Vite
│   ├── src/
│   └── Dockerfile
├── env/                  # Variables par service (db, backend, pgadmin)
└── docker-compose.yml
```
