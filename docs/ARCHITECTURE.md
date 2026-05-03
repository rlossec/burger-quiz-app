# Architecture High Level

Vue d'ensemble de l'architecture du projet Burger Quiz.

---

## Stack technique

| Composant           | Technologie                                  |
| ------------------- | -------------------------------------------- |
| **Backend**         | Django 6, Django REST Framework, Python 3.12 |
| **Frontend**        | React 19, TypeScript, Vite 7                 |
| **Base de données** | PostgreSQL 18                                |
| **Infrastructure**  | Docker Compose                               |

---

## Flux global

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │ ───► │   Frontend  │ ───► │   Backend   │ ───► │  PostgreSQL │
│ (navigateur)│      │ React/Vite  │      │ Django/DRF  │      │     18      │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
```

---

## Structure du projet

```
burger-quiz-app/
├── backend/                 # API Django
│   ├── src/
│   │   ├── config/          # Settings, URLs
│   │   ├── accounts/        # App utilisateurs (CustomUser, JWT, Djoser)
│   │   ├── quiz/            # App quiz (questions, manches, Burger Quiz)
│   │   ├── fixtures/        # Données JSON (monté en volume)
│   │   └── manage.py
│   └── Dockerfile
│
├── frontend/                # Interface React
│   ├── src/
│   └── Dockerfile
│
├── env/                     # Variables d'environnement par service
│   ├── db.env
│   ├── backend.env
│   └── pgadmin.env
│
├── docs/                    # Documentation
│   ├── README.md
│   ├── GETTING_STARTED.md
│   ├── ARCHITECTURE.md
│   ├── current/
│   ├── backend/
│   ├── frontend/
│   ├── database/
│   └── tests/
│
└── docker-compose.yml
```

---

## Services Docker

| Service      | Port                           | Rôle                                       |
| ------------ | ------------------------------ | ------------------------------------------ |
| **db**       | 5433 (hôte) → 5432 (conteneur) | PostgreSQL 18                              |
| **backend**  | 8000                           | Django + DRF, API REST                     |
| **frontend** | 5173                           | Vite dev server                            |
| **pgadmin**  | 5050                           | Outil d'administration DB (profil `tools`) |

---

## API REST

- **Base URL** : `/api/`
- **Authentification** : JWT Bearer (`Authorization: Bearer <access_token>`)
- **Endpoints** :
  - `auth/` : JWT, utilisateurs, activation, reset password (Djoser)
  - `quiz/` : questions, manches (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort), Burger Quiz

→ Référence détaillée : [backend/api-reference.md](backend/api-reference.md)

---

## Modèles principaux (Quiz)

- **Question** : énoncé, type (NU, SP, ME, AD, DB), réponses, médias
- **Manches** : Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger
- **MenuTheme** : thème (CL ou TR) pour la manche Menus
- **BurgerQuiz** : assemblage de manches (toss, nuggets, sel ou poivre, menus, addition, burger de la mort)

→ Détail : [database/models/README.md](database/models/README.md)

---

## Évolutions prévues

- **V0.1** : Authentication with email confirmation
- **V0.1** : Parcours frontend complet (création, édition, liste Burger Quiz)
- **V0.2** : Session de jeu (flow de l'émission, présentateur)
- **Plus tard** : Animations, scores, buzzer, réponses joueurs via l'interface
