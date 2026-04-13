# Tests — Structure du Burger Quiz

Ce document décrit les **cas couverts par les tests** pour les endpoints de structure du Burger Quiz, en lien avec la spécification API **[§ 3.9 Burger Quiz structure](../backend/api-reference.md#39-burger-quiz-structure)**.

**Fichier de tests** : `backend/src/quiz/tests/burger_quizzes/test_structure.py`  
**Commande** :

```bash
uv run python manage.py test quiz.tests.burger_quizzes.test_structure
# depuis backend/src
```

---

## Endpoints

| Méthode | Chemin                                     | Rôle                                               |
| ------- | ------------------------------------------ | -------------------------------------------------- |
| `GET`   | `/api/quiz/burger-quizzes/{id}/structure/` | Lire la structure (ordre, types, objets imbriqués) |
| `PUT`   | `/api/quiz/burger-quizzes/{id}/structure/` | Remplacer entièrement la structure                 |

Authentification : IsAuthenticated

## Matrice des cas (tests ↔ comportement attendu)

### Lecture (`GET`)

| Cas                                                                                                                   | Statut | Méthode de test                                      |
| --------------------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------- |
| Structure par défaut après `create_full` : 5 manches dans l’ordre NU → SP → ME → AD → DB                              | 200    | `test_get_structure_default_order`                   |
| Ordre persisté reflété dans `elements` (y compris interludes avant/après manches)                                     | 200    | `test_get_structure_with_custom_rows`                |
| `order` dans la réponse suit l’ordre en base (pas forcément l’ordre de création des types)                            | 200    | `test_get_structure_elements_ordered`                |
| Chaque élément inclut `order`, `type`, `id` et l’objet détaillé sous la clé du type (`nuggets`, `video_interlude`, …) | 200    | `test_get_structure_elements_include_nested_payload` |
| Burger Quiz inexistant                                                                                                | 404    | `test_get_structure_not_found`                       |
| Requête non authentifiée                                                                                              | 401    | `test_get_structure_requires_authentication`         |

### Mise à jour (`PUT`)

| Cas                                                                                                       | Statut | Méthode de test                                  |
| --------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------ |
| Remplacement complet : intro + 5 manches + pubs + outro (payload complet)                                 | 200    | `test_put_structure_success`                     |
| `PUT` supprime les anciennes lignes et ne garde que le nouveau tableau                                    | 200    | `test_put_structure_replaces_existing`           |
| Rang `order` = position dans le tableau (1 = premier élément)                                             | 200    | `test_put_structure_order_from_array_position`   |
| Structure vide `{"elements": []}` : plus aucun `BurgerQuizElement` ; `GET` suivant renvoie `[]`           | 200    | `test_put_structure_empty_elements`              |
| Référencer une manche **Nuggets** appartenant à un autre quiz (pas d’attache obligatoire au quiz courant) | 200    | `test_put_structure_any_nuggets_allowed`         |
| Plusieurs entrées `video_interlude` avec le **même** `VideoInterlude`                                     | 200    | `test_put_structure_multiple_interludes_allowed` |
| Même **slug** de manche deux fois (ex. deux `nuggets`)                                                    | 400    | `test_put_structure_duplicate_round_error`       |
| Interlude : `id` aléatoire inexistant                                                                     | 400    | `test_put_structure_interlude_not_found_error`   |
| Burger Quiz inexistant                                                                                    | 404    | `test_put_structure_not_found`                   |
| Requête non authentifiée                                                                                  | 401    | `test_put_structure_requires_authentication`     |

### Validation du corps `PUT` (erreurs 400)

Les messages exacts sont produits par `parse_structure_element` et `BurgerQuizStructureSerializer` (`burger_quiz_element.py`).

| Cas                                                                                                        | Statut | Méthode de test                                          |
| ---------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------- |
| Corps sans clé `elements`                                                                                  | 400    | `test_put_structure_missing_elements_key`                |
| `elements` n’est pas une liste                                                                             | 400    | `test_put_structure_elements_not_a_list`                 |
| Un élément du tableau n’est pas un objet                                                                   | 400    | `test_put_structure_element_not_an_object`               |
| `type` inconnu (hors `nuggets`, `salt_or_pepper`, `menus`, `addition`, `deadly_burger`, `video_interlude`) | 400    | `test_put_structure_unknown_type`                        |
| `type` absent                                                                                              | 400    | `test_put_structure_missing_type`                        |
| `id` absent                                                                                                | 400    | `test_put_structure_missing_id`                          |
| `id` mal formé (pas un UUID)                                                                               | 400    | `test_put_structure_invalid_uuid`                        |
| `type` = `salt_or_pepper` mais `id` est celui d’un **Nuggets** (mauvais modèle)                            | 400    | `test_put_structure_id_wrong_model_for_type`             |
| `type` = `video_interlude` mais `id` pointe vers une manche (ex. Nuggets)                                  | 400    | `test_put_structure_video_interlude_id_is_not_interlude` |
| `type` = `nuggets` et UUID sans ligne **Nuggets** correspondante                                           | 400    | `test_put_structure_round_id_not_found`                  |

---

## Règles métier rappelées (côté API)

- **Ordre implicite** : la position dans `elements` définit `order` (1…n).
- **Manches** : chaque slug de manche (`nuggets`, etc.) ne peut apparaître **qu’une fois** ; le même UUID de manche ne peut pas être dupliqué.
- **Interludes** : le même `VideoInterlude` peut être réutilisé plusieurs fois dans la liste.
- **`id` pour une manche** : UUID aligné avec le registre `Round` et la manche concrète (Nuggets, …) — voir commentaire modèle `Round` et signaux dans `quiz/signals.py`.

Pour le détail des champs de réponse et du corps de requête, se reporter à **[api-reference.md § 3.9](../backend/api-reference.md#39-burger-quiz-structure)**.
