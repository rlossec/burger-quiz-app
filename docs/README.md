# Documentation Burger Quiz 🍔

Point d'entrée de la documentation du projet Burger Quiz.

---

## Vision et suivi

| Document                                 | Rôle                                      |
| ---------------------------------------- | ----------------------------------------- |
| [current/PROJECT.md](current/PROJECT.md) | Vision, état actuel, priorités            |
| [current/ROADMAP.md](current/ROADMAP.md) | Étapes globales, versions cibles          |
| [current/BACKLOG.md](current/BACKLOG.md) | User stories, epics, parcours utilisateur |
| [current/TASKS.md](current/TASKS.md)     | Tâches techniques et idées à traiter      |
| [current/IDEAS.md](current/IDEAS.md)     | Idées et améliorations non priorisées     |

---

## Démarrage et architecture

| Document                                 | Rôle                                   |
| ---------------------------------------- | -------------------------------------- |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Installation, lancement, premier usage |
| [ARCHITECTURE.md](ARCHITECTURE.md)       | Stack, flux, structure du projet       |

---

## Spécifications techniques

| Domaine             | Document                                                 | Rôle                                                           |
| ------------------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| **Backend**         | [backend/api-reference.md](backend/api-reference.md)     | Référence API (Accounts + Quiz, endpoints, corps, contraintes) |
| **Frontend**        | [frontend/page_reference.md](frontend/page_reference.md) | Pages et flux utilisateur                                      |
| **Frontend**        | [frontend/components.md](frontend/components.md)         | Composants réutilisables (InlineForm, modales)                 |
| **Frontend**        | [frontend/wireframes/README.md](frontend/wireframes/README.md) | Wireframes (maquettes fil de fer, index)                        |
| **Base de données** | [database/models/README.md](database/models/README.md)   | Modèles, règles métier (original, réutilisabilité)             |
| **Base de données** | [database/fixtures.md](database/fixtures.md)             | Fixtures Django, chargement, export                            |

---

## Tests

| Document                                           | Rôle                                                      |
| -------------------------------------------------- | --------------------------------------------------------- |
| [tests/README.md](tests/README.md)                 | Stratégie de tests, point d'entrée vers les docs de tests |
| [tests/quiz.md](tests/quiz.md)                     | Tests du module Quiz (endpoints, structure)               |
| [tests/quiz-factories.md](tests/quiz-factories.md) | Factories (factory_boy) pour les tests Quiz               |
| [tests/accounts.md](tests/accounts.md)             | Tests du module Accounts (auth, users)                    |

---

## Structure des dossiers

```
docs/
├── README.md              ← Vous êtes ici
├── GETTING_STARTED.md
├── ARCHITECTURE.md
├── current/               # Suivi projet
│   ├── PROJECT.md
│   ├── ROADMAP.md
│   ├── BACKLOG.md
│   ├── TASKS.md
│   └── IDEAS.md
├── backend/               # API
│   └── api-reference.md
├── frontend/              # UI
│   ├── page_reference.md
│   ├── components.md
│   └── wireframes/        # Maquettes par domaine
│       ├── README.md
│       ├── layout-login.md
│       ├── questions.md
│       ├── nuggets.md
│       ├── salt-or-pepper.md
│       ├── menus-menutheme.md
│       ├── addition.md
│       ├── deadly-burger.md
│       ├── burger-quiz.md
│       └── modals.md
├── database/              # Modèles et données
│   ├── models/
│   │   ├── README.md
│   │   └── uml.mermaid
│   └── fixtures.md
└── tests/                 # Documentation des tests
    ├── README.md          # Stratégie, point d'entrée
    ├── quiz.md
    ├── quiz-factories.md
    └── accounts.md
```
