# Stratégie de tests

Point d'entrée de la documentation des tests Burger Quiz.

---

## Principes

- **Backend** : tests d'intégration API (Django TestCase) alignés sur [api-reference.md](../backend/api-reference.md)
- **Organisation** : un fichier par endpoint ou par ressource, dossiers par module
- **Données** : factories (factory_boy) pour isoler les tests et éviter la duplication

---

## Documentation par module

| Module       | Document                               | Contenu                                                                     |
| ------------ | -------------------------------------- | --------------------------------------------------------------------------- |
| **Quiz**     | [quiz.md](quiz.md)                     | Tests des endpoints (questions, manches, Burger Quiz), structure, commandes |
| **Quiz**     | [quiz-factories.md](quiz-factories.md) | Factories factory_boy, méthodes, exemples d'usage                           |
| **Accounts** | [accounts.md](accounts.md)             | Tests auth (JWT, activation, reset), CRUD utilisateurs                      |

---

## Exécution globale

```bash
# Tous les tests (depuis backend/src)
uv run manage.py test

# Avec Docker
docker compose exec backend uv run python manage.py test
```

---

## Par module

| Module   | Commande                               |
| -------- | -------------------------------------- |
| Quiz     | `uv run manage.py test quiz.tests`     |
| Accounts | `uv run manage.py test accounts.tests` |

→ Détail des commandes et structure dans chaque document ci-dessus.
