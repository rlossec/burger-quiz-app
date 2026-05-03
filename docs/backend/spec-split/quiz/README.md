# Quiz — index API

Préfixe : **`/api/quiz/`** (sous-chemins par ressource).

---

## Fichiers par groupe

| Fichier | Périmètre |
| --- | --- |
| [`questions.md`](questions.md) | `/api/quiz/questions/` (liste, détail, CRUD) |
| [`nuggets.md`](nuggets.md) | `/api/quiz/nuggets/` |
| [`salt-or-pepper.md`](salt-or-pepper.md) | `/api/quiz/salt-or-pepper/` |
| [`menus.md`](menus.md) | `/api/quiz/menu-themes/` + `/api/quiz/menus/` |
| [`additions.md`](additions.md) | `/api/quiz/additions/` |
| [`deadly-burger.md`](deadly-burger.md) | `/api/quiz/deadly-burgers/` |
| [`quizzes.md`](quizzes.md) | `/api/quiz/burger-quizzes/` |
| [`contraintes.md`](contraintes.md) | Contraintes métier, flux, récap (transverse) |

---

## Endpoints — récapitulatif

| Méthode | Chemin | Description | Documentation |
| --- | --- | --- | --- |
| `GET` | `/api/quiz/questions/` | Liste paginée (filtres) | [`questions.md`](questions.md) |
| `GET` | `/api/quiz/questions/{id}/` | Détail + réponses | [`questions.md`](questions.md) |
| `POST` | `/api/quiz/questions/` | Création | [`questions.md`](questions.md) |
| `PUT` | `/api/quiz/questions/{id}/` | Remplacement complet | [`questions.md`](questions.md) |
| `PATCH` | `/api/quiz/questions/{id}/` | Mise à jour partielle | [`questions.md`](questions.md) |
| `DELETE` | `/api/quiz/questions/{id}/` | Suppression | [`questions.md`](questions.md) |
| `GET` | `/api/quiz/nuggets/` | Liste manches Nuggets | [`nuggets.md`](nuggets.md) |
| `GET` | `/api/quiz/nuggets/{id}/` | Détail | [`nuggets.md`](nuggets.md) |
| `POST` | `/api/quiz/nuggets/` | Création | [`nuggets.md`](nuggets.md) |
| `PATCH` \| `PUT` | `/api/quiz/nuggets/{id}/` | Mise à jour | [`nuggets.md`](nuggets.md) |
| `DELETE` | `/api/quiz/nuggets/{id}/` | Suppression | [`nuggets.md`](nuggets.md) |
| `GET` | `/api/quiz/salt-or-pepper/` | Liste | [`salt-or-pepper.md`](salt-or-pepper.md) |
| `GET` | `/api/quiz/salt-or-pepper/{id}/` | Détail | [`salt-or-pepper.md`](salt-or-pepper.md) |
| `POST` | `/api/quiz/salt-or-pepper/` | Création | [`salt-or-pepper.md`](salt-or-pepper.md) |
| `PATCH` \| `PUT` | `/api/quiz/salt-or-pepper/{id}/` | Mise à jour | [`salt-or-pepper.md`](salt-or-pepper.md) |
| `DELETE` | `/api/quiz/salt-or-pepper/{id}/` | Suppression | [`salt-or-pepper.md`](salt-or-pepper.md) |
| `GET` | `/api/quiz/menu-themes/` | Liste thèmes | [`menus.md`](menus.md) |
| `GET` | `/api/quiz/menu-themes/{id}/` | Détail thème | [`menus.md`](menus.md) |
| `POST` | `/api/quiz/menu-themes/` | Création thème | [`menus.md`](menus.md) |
| `PUT` \| `PATCH` | `/api/quiz/menu-themes/{id}/` | Mise à jour thème | [`menus.md`](menus.md) |
| `DELETE` | `/api/quiz/menu-themes/{id}/` | Suppression thème | [`menus.md`](menus.md) |
| `GET` | `/api/quiz/menus/` | Liste manches Menus | [`menus.md`](menus.md) |
| `GET` | `/api/quiz/menus/{id}/` | Détail manche Menus | [`menus.md`](menus.md) |
| `POST` | `/api/quiz/menus/` | Création manche Menus | [`menus.md`](menus.md) |
| `PUT` \| `PATCH` \| `DELETE` | `/api/quiz/menus/{id}/` | Mise à jour / suppression | [`menus.md`](menus.md) |
| `GET` | `/api/quiz/additions/` | Liste | [`additions.md`](additions.md) |
| `GET` | `/api/quiz/additions/{id}/` | Détail | [`additions.md`](additions.md) |
| `POST` | `/api/quiz/additions/` | Création | [`additions.md`](additions.md) |
| `PUT` \| `PATCH` | `/api/quiz/additions/{id}/` | Mise à jour | [`additions.md`](additions.md) |
| `DELETE` | `/api/quiz/additions/{id}/` | Suppression | [`additions.md`](additions.md) |
| `GET` | `/api/quiz/deadly-burgers/` | Liste | [`deadly-burger.md`](deadly-burger.md) |
| `GET` | `/api/quiz/deadly-burgers/{id}/` | Détail | [`deadly-burger.md`](deadly-burger.md) |
| `POST` | `/api/quiz/deadly-burgers/` | Création | [`deadly-burger.md`](deadly-burger.md) |
| `PUT` \| `PATCH` | `/api/quiz/deadly-burgers/{id}/` | Mise à jour | [`deadly-burger.md`](deadly-burger.md) |
| `DELETE` | `/api/quiz/deadly-burgers/{id}/` | Suppression | [`deadly-burger.md`](deadly-burger.md) |
| `GET` | `/api/quiz/burger-quizzes/` | Liste | [`quizzes.md`](quizzes.md) |
| `GET` | `/api/quiz/burger-quizzes/{id}/` | Détail | [`quizzes.md`](quizzes.md) |
| `POST` | `/api/quiz/burger-quizzes/` | Création | [`quizzes.md`](quizzes.md) |
| `PUT` \| `PATCH` | `/api/quiz/burger-quizzes/{id}/` | Mise à jour | [`quizzes.md`](quizzes.md) |
| `DELETE` | `/api/quiz/burger-quizzes/{id}/` | Suppression | [`quizzes.md`](quizzes.md) |
| — | — | Contraintes, flux, champs calculés (récap) | [`contraintes.md`](contraintes.md) |

Champs calculés détaillés : monolithe [`../api-specifications.md`](../api-specifications.md) §2.9 et [`../api-endpoints-et-contraintes.md`](../api-endpoints-et-contraintes.md) §7.1.
