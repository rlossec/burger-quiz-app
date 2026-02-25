# Wireframes — Burger de la mort

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [DeadlyBurgerListPage](#deadlyburgerlistpage)
- [DeadlyBurgerDetailPage](#deadlyburgerdetailpage)
- [DeadlyBurgerCreatePage / DeadlyBurgerEditPage](#deadlyburgercreatepage--deadlyburgereditpage)

---

## DeadlyBurgerListPage

### Principe

Tableau des manches Burger de la mort : colonnes titre, original ?, nombre d’utilisation. Bouton Ajouter → DeadlyBurgerCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

Colonnes : Titre | Original ? | Utilisations | Actions.

### Appels API

| Action | Méthode | Endpoint | Réf. |
| ------ | ------- | -------- | ---- |
| Lister | GET | `/api/quiz/deadly-burgers/` | [api-reference](../../../backend/api-reference.md) §2.6 |

---

## DeadlyBurgerDetailPage

### Principe

Affichage : titre, liste des 10 questions dans l’ordre (type DB, pas de réponses à afficher). Actions : DeadlyBurgerEditPage, suppression (modale).

### Wireframe

_(Liste titre + 10 questions.)_

### Appels API

| Action | Méthode | Endpoint | Réf. |
| ------ | ------- | -------- | ---- |
| Détail | GET | `/api/quiz/deadly-burgers/{id}/` | [api-reference](../../../backend/api-reference.md) §2.6 |

---

## DeadlyBurgerCreatePage / DeadlyBurgerEditPage

### Principe

Formulaire : titre. **10 questions** exactement (type DB), ordre fixe. Pas de réponses à saisir pour DB. Contrainte API : 10 questions, type DB. **Questions réutilisables** : on peut piocher dans les questions existantes.

**Piocher dans les questions existantes** : le bouton « Remplir avec des questions existantes » ouvre une **modale** ([modale ajout question](../modals.md)) avec recherche et filtre type DB. On sélectionne des questions ; les IDs sont **ajoutés à la liste** du formulaire (ordre 1 à 10). À la **soumission** du formulaire parent, on envoie `question_ids` à l'API (une seule requête).

### Wireframe

```
+------------------------------------------------------------------+
|  Créer/Modifier un Burger de la mort                              |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]        |
|  Questions (exactement 10, type DB)                               |
|  | 1  | [___________________________________________] [👁][🗑]    |
|  | 2  | [___________________________________________] [👁][🗑]    |
|  | ...|  (énoncé ou « question existante » + [👁] pour détail)   |
|  | 10 | [___________________________________________] [👁][🗑]    |
|  [ Remplir avec des questions existantes ]  (ouvre modale recherche) |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint | Réf. |
| ------ | ------- | -------- | ---- |
| Créer | POST | `/api/quiz/deadly-burgers/` | [api-reference](../../../backend/api-reference.md) §2.6 |
| Modifier | PUT/PATCH | `/api/quiz/deadly-burgers/{id}/` | idem |
| Questions (liste / recherche type DB) | GET | `/api/quiz/questions/?question_type=DB&search=...` | §2.1 |
