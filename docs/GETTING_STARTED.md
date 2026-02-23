# Getting Started

Guide pour installer et lancer l'application Burger Quiz.

---

## Prérequis

- **Docker** et **Docker Compose**
- (Optionnel) Git pour cloner le dépôt

---

## 1. Cloner le projet

```bash
git clone <url-du-repo>
cd burger-quiz-app
```

---

## 2. Configurer l'environnement

Les variables d'environnement sont définies par service dans le dossier `env/`. Copiez les fichiers d'exemple :

```bash
cp env/db.env.example env/db.env
cp env/backend.env.example env/backend.env
cp env/pgadmin.env.example env/pgadmin.env
```

### Superuser Django (recommandé)

Pour créer automatiquement un compte administrateur au démarrage, définissez dans `env/backend.env` :

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

→ Voir [env/README.md](../env/README.md) pour le détail des variables.

---

## 3. Lancer l'application

```bash
docker compose up -d
```

Les migrations et la création du superuser (si configuré) sont exécutées automatiquement au démarrage du backend.

### Avec pgAdmin (optionnel)

```bash
docker compose --profile tools up -d
```

---

## 4. Accès aux services

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **Django Admin** | http://localhost:8000/admin/ |
| **pgAdmin** | http://localhost:5050 |

---

## 5. Charger les fixtures (données de démo)

Les commandes Django s'exécutent **dans le conteneur backend** :

```bash
docker compose exec backend uv run python manage.py loaddata fixtures/quiz_data.json
```

→ Voir [database/fixtures.md](database/fixtures.md) pour plus de détails.

---

## 6. Premier usage

1. **Connexion admin** : allez sur http://localhost:8000/admin/ avec le superuser créé.
2. **API** : l'authentification est en JWT. Obtenir un token : `POST /api/auth/jwt/create/` avec `username` et `password`.
3. **Documentation API** : voir [backend/api-reference.md](backend/api-reference.md) pour la liste des endpoints.

---

## Dépannage

- **Port déjà utilisé** : modifiez `POSTGRES_PORT` ou `PGADMIN_PORT` dans `env/db.env` ou `env/pgadmin.env`.
- **Backend ne démarre pas** : vérifiez que la base PostgreSQL est en bonne santé (`docker compose ps`).
- **Migrations manquantes** : `docker compose exec backend uv run python manage.py migrate` (normalement automatique).
