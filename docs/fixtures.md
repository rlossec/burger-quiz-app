# Fixtures Django

## Volume monté

Le dossier `backend/src/fixtures` est monté à l'intérieur du conteneur backend via Docker Compose :

```yaml
volumes:
  - ./backend/src/fixtures:/app/fixtures
```

Les fichiers de fixtures sont donc accessibles dans le conteneur au chemin `/app/fixtures`, et toute modification faite depuis le conteneur se reflète immédiatement sur l'hôte (et inversement).

## Exécution des commandes dans le conteneur

Les commandes Django `loaddata` et `dumpdata` doivent être exécutées **à l'intérieur du conteneur backend** (puisque la base de données et l'environnement Django y sont configurés).

Utilisez `docker compose exec backend` pour lancer une commande dans le conteneur :

### Charger les fixtures (loaddata)

```bash
docker compose exec backend uv run python manage.py loaddata fixtures/quiz_data.json
```

### Exporter les données (dumpdata)

À exécuter depuis la racine du projet (la redirection `>` est interprétée par le shell hôte) :

```bash
docker compose exec backend uv run python manage.py dumpdata --indent 2 quiz > backend/src/fixtures/quiz_data.json
```

## Fichiers de fixtures

| Fichier | Description |
|---------|-------------|
| `quiz_data.json` | Données du quiz (questions, réponses, etc.) |
