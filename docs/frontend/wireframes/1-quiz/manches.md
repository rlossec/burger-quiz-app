# Wireframes — Manches (hub)

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [ManchesHubPage](#1-mancheshubpage)

---

## 1 - ManchesHubPage

### Principe

Page d'entrée unique pour accéder à toutes les familles de manches :

- Nuggets
- Sel ou Poivre
- Menus
- Addition
- Burger de la mort
- Interludes

Chaque carte affiche un mini-récap opérationnel :

- **Créées** : nombre total de manches de ce type.
- **Utilisées** : nombre de manches présentes dans au moins un Burger Quiz (structure).
- **Non utilisées** : `créées - utilisées` (utile pour nettoyage ou réaffectation).

La page sert de **hub de navigation** vers chaque `*ListPage`.

### Wireframe

```
+-----------------------------------------------------------------------------------------+
|  Manches                                                           [ + Créer manche ]   |
+-----------------------------------------------------------------------------------------+
|  Rechercher un type... [________________________]                                       |
|                                                                                         |
|  ┌──────────────────────────┐  ┌─────────────────────────┐  ┌───────── ───────────────┐ |
|  |  🍗 Nuggets              |  |  🧂 Sel ou Poivr       |  |  🍽️ Menus               | |
|  |  Créées       : 42       |  |  Créées       : 18      |  |  Créées       : 27      | |
|  |  Utilisées    : 31       |  |  Utilisées    : 14      |  |  Utilisées    : 19      | |
|  |  Non utilisées: 11       |  |  Non utilisées: 4       |  |  Non utilisées: 8       | |
|  |                          |  |                         |  |                         | |
|  |  [Voir la liste]         |  |  [Voir la liste]        |  |  [Voir la liste]        | |
|  └──────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘ |
|                                                                                         |
|  ┌─────────────────────────┐  ┌──────────────────────────┐  ┌─────────────────────────┐ |
|  |  ➕ Addition            |  |  💀 Burger de la mort    |  |  🎬 Interludes         | |
|  |  Créées       : 23      |  |  Créées       : 9        |  |  Créées       : 35      | |
|  |  Utilisées    : 20      |  |  Utilisées    : 9        |  |  Utilisées    : 12      | |
|  |  Non utilisées: 3       |  |  Non utilisées: 0        |  |  Non utilisées: 23      | |
|  |                         |  |                          |  |                         | |
|  |  [Voir la liste]        |  |  [Voir la liste]         |  |  [Voir la liste]        | |
|  └─────────────────────────┘  └──────────────────────────┘  └─────────────────────────┘ |
+-----------------------------------------------------------------------------------------+
```

### Flux principal

```
[ManchesHubPage]
      │
      ├── clic "Voir la liste" sur Nuggets         ──> [NuggetsListPage]
      ├── clic "Voir la liste" sur Sel ou Poivre   ──> [SaltPepperListPage]
      ├── clic "Voir la liste" sur Menus           ──> [MenusListPage]
      ├── clic "Voir la liste" sur Addition        ──> [AdditionListPage]
      ├── clic "Voir la liste" sur Burger de la mort ─> [DeadlyBurgerListPage]
      └── clic "Voir la liste" sur Interludes      ──> [InterludesListPage]
```

### Données / calcul des stats

- **Créées** : taille de la liste du type concerné.
- **Utilisées** : nombre d'IDs distincts de ce type trouvés dans les structures des Burger Quiz.
- **Non utilisées** : `max(0, créées - utilisées)`.

Exemple de logique métier :

```ts
created = items.length;
used = countDistinctIdsReferencedInQuizStructures(typeSlug);
unused = Math.max(0, created - used);
```

### Appels API

| Besoin                   | Endpoint                        | Usage                        |
| ------------------------ | ------------------------------- | ---------------------------- |
| Lister Burger Quiz       | `GET /api/quiz/burger-quizzes/` | Lire `structure` pour usages |
| Lister Nuggets           | `GET /api/quiz/nuggets/`        | Compter `créées`             |
| Lister Sel ou Poivre     | `GET /api/quiz/salt-or-pepper/` | Compter `créées`             |
| Lister Menus             | `GET /api/quiz/menus/`          | Compter `créées`             |
| Lister Addition          | `GET /api/quiz/additions/`      | Compter `créées`             |
| Lister Burger de la mort | `GET /api/quiz/deadly-burgers/` | Compter `créées`             |
| Lister Interludes        | `GET /api/quiz/interludes/`     | Compter `créées`             |

> Variante plus performante possible plus tard : endpoint backend de stats agrégées.

### États UI à prévoir

- **Loading** : skeleton des 6 cartes.
- **Error** : message global + bouton "Réessayer".
- **Empty global** : aucune manche créée.
- **Empty par type** : carte affichée avec `Créées: 0`, `Utilisées: 0`, `Non utilisées: 0`.
