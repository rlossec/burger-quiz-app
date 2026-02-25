# Composants et patterns frontend

Ce document décrit les composants réutilisables et les patterns d’interface imaginés pour les pages du frontend. Structure des pages : [page_reference.md](page_reference.md). Wireframes : [wireframes/README.md](wireframes/README.md).

---

## Questions

### QuestionsInlineForm

Pattern d’ajout de **questions** directement dans un formulaire de création/édition de manche, sans quitter la page.

#### Principe

- Chaque ligne = une question (énoncé + réponses selon le type).
- Le **`question_type`** est **prérempli** selon la page (NU, SP, ME, AD, DB) et non modifiable dans l’inline.
- Actions : **ajouter** une ligne (nouvelle question inline), **supprimer** une ligne (avec confirmation si besoin).
- A arbitrer : À la soumission du formulaire parent : création des questions puis de la manche (ou mise à jour) ou soumission indépendante ?

#### Piocher dans les questions existantes (Nuggets, Deadly Burger)

**Modale indépendante** (« Ajouter des questions ») avec **outil de recherche** (champ recherche + filtre type). Les questions sélectionnées sont ajoutées à la liste du formulaire ; les **IDs sont envoyés à la soumission** du formulaire parent (pas de sauvegarde dans la modale). Voir [wireframes modale ajout question](wireframes/modals.md). Pour Nuggets : les questions **déjà dans la manche** sont **grisées** dans la modale pour éviter les doublons.

#### Par type de manche

| Page                              | question_type | Nombre / contraintes                                        | Remarques                                                                                                                                   |
| --------------------------------- | ------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **NuggetsCreatePage / Edit**      | NU            | Nombre **pair** (ex. 6 champs possibles), 2 par 2 par ligne | Sélection (modale recherche) ou création inline. Une question déjà choisie peut être grisée dans la modale pour éviter les doublons.       |
| **SaltOrPepperCreatePage / Edit** | SP            | Variable                                                    | Champs « propositions » (2 à 5) en haut ; chaque question a sa réponse dans un **déroulant** = une des propositions.                        |
| **MenuThemeCreatePage / Edit**    | ME            | Variable                                                    | InlineForm pour les questions du thème.                                                                                                     |
| **AdditionCreatePage / Edit**     | AD            | 8 inline form par défaut, ajout/suppression possible        | InlineForm avec question_type = AD.                                                                                                         |
| **DeadlyBurgerCreatePage / Edit** | DB            | **10** questions exactement                                 | 10 InlineForm fixes, question_type = DB.                                                                                                    |

#### Champs communs (par ligne question)

- Énoncé (texte).
- Réponses : selon le type (NU : 4 réponses + 1 correcte ; SP : choix parmi les propositions de la manche ; ME : 1 réponse ; AD : 1 réponse ; DB : pas de réponses côté formulaire).
- Optionnel : **original** (case à cocher), **video_url**, **image_url**, **explanations** (selon la page).

### Ajout / suppression de lignes

- **Ajouter** : bouton « Ajouter une question » (ou équivalent) qui ajoute une ligne d’inline form.
- **Supprimer** : icône/bouton (ex. poubelle) sur chaque ligne, avec éventuelle modale de confirmation.
- Contraintes à respecter côté UI : minimum 2 propositions pour Sel ou poivre ; nombre pair pour Nuggets ; exactement 10 pour DeadlyBurger.

---

## Autres composants (à préciser)

- **Modale de confirmation** : suppression manche, suppression question inline.
- **Liste déroulante de manches** : pour BurgerQuizCreate (nuggets_id, salt_or_pepper_id, etc.) et MenuCreatePage (menu_1_id, menu_2_id, menu_troll_id).
