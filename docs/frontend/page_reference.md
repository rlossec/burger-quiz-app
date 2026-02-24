# Liste des pages

Structure des pages imaginées pour le frontend. Composants réutilisables (InlineForm, modales, etc.) : [components.md](components.md). Maquettes fil de fer : [wireframes/README.md](wireframes/README.md).

---

## Avancement des pages

_À mettre à jour au fur et à mesure : **Idée** | **Wireframe** | **Implémenté**_

| Zone | Avancement | Maquette |
|------|------------|----------|
| Layout + Login | Wireframe | [layout-login.md](wireframes/layout-login.md) |
| Questions | Wireframe | [questions.md](wireframes/questions.md) |
| Nuggets | Wireframe | [nuggets.md](wireframes/nuggets.md) |
| Sel ou Poivre | Wireframe | [salt-or-pepper.md](wireframes/salt-or-pepper.md) |
| Menus + MenuTheme | Wireframe | [menus-menutheme.md](wireframes/menus-menutheme.md) |
| Addition | Wireframe | [addition.md](wireframes/addition.md) |
| Burger de la mort | Wireframe | [deadly-burger.md](wireframes/deadly-burger.md) |
| Burger Quiz | Wireframe | [burger-quiz.md](wireframes/burger-quiz.md) |
| Modales | Wireframe | [modals.md](wireframes/modals.md) |

---

## Question

- QuestionsListPage : Liste les questions avec des filtres de type, original.
- QuestionDetailPage : Détail d’une question (énoncé, réponses, type, original, médias).
- QuestionCreatePage : Création d’une question (type, énoncé, réponses, original, video_url, image_url).
- QuestionEditPage : Édition de la question sélectionnée.

### QuestionsListPage

Liste les questions avec des filtres par **type** (NU, SP, ME, AD, DB), **original** (true/false). Colonnes possibles : texte (aperçu), type, original ?, nombre d'utilisations, nombre d’utilisations. Actions : accès au détail, édition, suppression (avec modale de confirmation). Bouton « Ajouter » pour aller vers QuestionCreatePage.

### QuestionDetailPage

Affichage en lecture seule : texte de la question, type, original ?, explications, liens vidéo/image, liste des réponses avec indication de la bonne réponse. Liens ou boutons vers QuestionEditPage et retour à la liste.

### QuestionCreatePage / QuestionEditPage

Formulaire : type de question (sélection), énoncé, original (case à cocher), explications optionnelles, video_url et image_url optionnels. Bloc réponses selon le type (ex. 4 réponses pour NU, 2 pour SP, etc.) avec indication de la réponse correcte.

## Nuggets

- NuggetsListPage : Liste des manche Nuggets disponibles
- NuggetsDetailPage : Detail de la manche Nuggets cliqué
- NuggetsCreatePage : Création d'une manche Nuggets
- NuggetsEditPage : Edition de la manche Nuggets cliqué

### NuggetsListPage

On peut imaginer un tableau listant les Manches nuggets créées, avec une colonne original ?, une colonne Utilisation (correspondant au nombre de fois où elle est dans un BurgerQuiz), et une colonne nbre de Nuggets. Enfin un bouton Ajouter en haut à droite du tableau permet d'aller vers la page de création.

### NuggetsCreatePage / NuggetsEditPage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Champs de sélection ou création inline de questions Nuggets, de base au nombre de 6, deux par deux par ligne. En effet comme on pose des questions à tour de rôle, il faut qu'on est des couples de questions.
Aussi on pourra penser à la contrainte que lorsqu'une manche est sélectionné elle soit grisée et non cliquable pour les autres champs de sélection.

> Backend : Penser à mettre dans API reference de vérifiez à la fois le fait qu'on soumette un nombre pair de question et qu'il n'y est pas deux fois la même question

Un bouton et une modale permettront d'ajouter des questions Nuggets et des boutons avec des icones pour aller vers SaltOrPepperDetailPage ou SaltOrPepperEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

## Sel ou Poivre

- SaltOrPepperListPage
- SaltOrPepperDetailPage
- SaltOrPepperCreatePage
- SaltOrPepperEditPage

### SaltOrPepperListPage

Liste les manches Sel ou poivre créé, avec de même que pour les Nuggets, des colonnes original ? et e nombre d'utilisation. Enfin un bouton ajouter pour conduire vers la page d'ajout `SaltOrPepperCreatePage` et des boutons avec des icones pour aller vers SaltOrPepperDetailPage ou SaltOrPepperEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

### SaltOrPepperCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire avec le nom de la manche, trois champs par défaut les uns à côté des autres pour les propositions de réponses. On aurait un bouton pour ajouter supprimer des champs(minumum deux champs, maximum 5 champs).

Enfin une succession de champs de questions avec la réponse étant un champ déroulant avec les propositions plus haut disponibles.
On aurait aussi un case Check pour dire si c'est une question originale ou non, à la fois au niveau de la manche (et du coup si coché toutes les questions seraient cochés et pas changeable) et au niveau question.

### SaltOrPepperDetailPage

Affichage en lecture : titre, description, liste des propositions (choice_labels), liste des questions avec la réponse correcte pour chacune. Indication « original ? » (valeur dérivée à partir des questions). Boutons vers SaltOrPepperEditPage et suppression (modale).

### SaltOrPepperEditPage

Même structure que SaltOrPepperCreatePage (titre, description, 2 à 5 propositions, questions avec réponse = un des choix). Contrainte API : réponses des questions cohérentes avec les propositions. Bouton/modale pour ajouter des questions Nuggets, icônes vers détail/édition question, poubelle avec confirmation.

## Menus

- MenuListPage
- MenuCreatePage
- MenuDetailPage
- MenuEditPage
- MenuThemeListPage
- MenuThemeDetailPage
- MenuThemeCreatePage
- MenuThemeEditPage

### MenuListPage

Dans la même configuration que pour les autres pages on aurait un listing des manche Menu avec la colonne "original ?" et "nombre d'utilisation".
On aurait ensuite un bouton Ajouter pour aller vers la page MenuCreatePage au dessus du listing, et des boutons avec des icones pour aller vers MenuDetailPage ou MenuEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

### MenuDetailPage

Affichage : titre, description, et les 3 thèmes (menu 1, menu 2, menu troll) avec pour chacun titre et type (CL/TR), liste des questions. Valeur dérivée « original ? ». Actions : MenuEditPage, suppression (modale).

### MenuCreatePage

Formulaire : titre, description optionnelle. Sélection des 3 thèmes : **menu 1** et **menu 2** (MenuTheme avec type CL), **menu troll** (MenuTheme avec type TR). Les thèmes doivent être créés au préalable (MenuThemeCreatePage) ou sélectionnés parmi la liste. Contrainte API : exactement 2 classiques + 1 troll, IDs distincts.

### MenuEditPage

Même champs que MenuCreatePage (titre, description, menu_1_id, menu_2_id, menu_troll_id). Réutilisation des mêmes contraintes.

### MenuThemeListPage

Liste des thèmes de menu (MenuTheme) avec colonnes : titre, type (CL / TR), original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → MenuThemeCreatePage. Actions : détail, édition, suppression (modale).

### MenuThemeDetailPage

Détail d’un thème : titre, type (Classique / Troll), liste ordonnée des questions. Actions : MenuThemeEditPage, suppression.

### MenuThemeCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, type (CL ou TR), liste ordonnée de questions (question_ids). Questions de type ME uniquement. Boutons/liens pour ajouter des questions, accéder à QuestionDetail/Edit, réordonner.

### MenuThemeEditPage

Même structure que MenuThemeCreatePage.

## Addition

- AdditionListPage
- AdditionCreatePage
- AdditionDetailPage
- AdditionEditPage

### AdditionListPage

Tableau des manches Addition avec colonnes : titre, original ?, nombre d’utilisation, nombre de questions. Bouton Ajouter → AdditionCreatePage. Icônes vers détail / édition, poubelle avec modale de confirmation.

### AdditionCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, description optionnelle, liste ordonnée de questions (question_ids). Questions de type AD uniquement (ex. 8 par défaut, ajout/suppression). Sélection parmi les questions existantes type AD (ou création inline selon choix métier).

### AdditionDetailPage

Affichage : titre, description, liste des questions dans l’ordre. Valeur dérivée. Actions : AdditionEditPage, suppression (modale).

### AdditionEditPage

Même champs que AdditionCreatePage.

## Burger de la mort

- DeadlyBurgerListPage
- DeadlyBurgerCreatePage
- DeadlyBurgerDetailPage
- DeadlyBurgerEditPage

### DeadlyBurgerListPage

Tableau des manches Burger de la mort : titre, original ?, nombre d’utilisation. Bouton Ajouter → DeadlyBurgerCreatePage. Actions : détail, édition, suppression (modale).

### DeadlyBurgerCreatePage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Formulaire : titre, **10 questions** exactement (type DB). Contrainte API : 10 questions, type DB. Questions réutilisables entre manches.

### DeadlyBurgerDetailPage

Affichage : titre, liste des 10 questions dans l’ordre. Actions : DeadlyBurgerEditPage, suppression (modale).

### DeadlyBurgerEditPage

Même structure que DeadlyBurgerCreatePage (toujours 10 questions type DB).

---

## Burger Quiz

1. BurgerQuizListPage : Liste des Burger Quiz créés.
2. BurgerQuizDetailPage : Détail d’un quiz (titre, toss, manches liées).
3. BurgerQuizCreatePage : Création d’un quiz (titre, toss, sélection des manches : nuggets, salt_or_pepper, menus, addition, deadly_burger).
4. BurgerQuizEditPage : Édition du quiz.

### 1. BurgerQuizListPage

On imagine une liste des burger quiz existant. On pourrait avoir une colonne indiquant son avancement (le nombre de manche fixé sur les requises : Toss, NU, ME, AD, )

### BurgerQuizListPage

Liste des sessions Burger Quiz : titre, date/création, manches incluses (aperçu). Bouton Créer. Actions : détail, édition, suppression.

### BurgerQuizDetailPage

Lecture : titre, toss, et pour chaque type de manche (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) affichage de la manche choisie (lien vers la ressource ou résumé).

### BurgerQuizCreatePage / BurgerQuizEditPage

Formulaire : titre, champ **toss** (optionnel). Champs optionnels : nuggets_id, salt_or_pepper_id, menus_id, addition_id, deadly_burger_id (listes déroulantes ou recherche vers les manches existantes). Au moins une manche recommandée.

---

## Alignement API / modèles (pour les pages ci‑dessus)

Les adaptations suivantes ont été prévues côté modèles et endpoints pour alimenter ces pages :

- **QuestionsListPage** : filtres `question_type` (NU, SP, ME, AD, DB) et `original` (true/false) ; champ calculé **`usage_count`** (nombre d’utilisations de la question dans les manches). « Original ? » = affichage du champ **`original`** (booléen).
- **Toutes les listes de manches** (Nuggets, Sel ou poivre, Menus, Addition, Burger de la mort) : champ calculé **`burger_quiz_count`** (ou `used_in_burger_quizzes_count`) pour la colonne « nombre d’utilisation » ; champ **`original`** (stocké sur la manche) pour « original ? ».
- **MenuThemeListPage** : champs calculés **`used_in_menus_count`** et **`questions_count`**.
- **BurgerQuizListPage** : **`created_at`** / **`updated_at`** sur le modèle BurgerQuiz pour « date/création » et tri. Réponse API : inclure ces champs.
- **Toss** : la page reference indique « toss optionnel » ; l’API peut le laisser obligatoire ou optionnel selon le choix métier (voir `docs/backend/api-reference.md` §2.7 Burger Quiz).

Détail des champs calculés et filtres : `docs/backend/api-reference.md` §2.9.
