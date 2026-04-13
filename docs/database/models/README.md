# Les modèles

## Sommaire

- [1. Vue générale](#1-vue-générale)
- [2. Question et réponses](#2-question-et-réponses)
- [3. Manches (modèles concrets)](#3-manches)
- [4. Interludes vidéo](#4-interludes-vidéo)
- [5. Burger Quiz et structure](#5-burger-quiz-et-structure)

## 1. Vue générale

### Esprit : manches concrètes et déroulé

Le quiz repose sur des **manches concrètes**, chacune modélisée par un type Django dédié : 
- **`Nuggets`**,
- **`SaltOrPepper`**,
- **`Menus`**,
- **`Addition`**,
- **`DeadlyBurger`**.

Les questions de type **menu** sont rattachées aux **`MenuTheme`** (trois thèmes par manche Menus : classique, classique, troll).

Pour la **structure** (ordre des segments dans un jeu), une ligne de registre **`Round`** est créée ou mise à jour par **signaux** à chaque sauvegarde d’une manche : même **UUID** que la manche, champ **`round_type`** (slugs du catalogue **`ROUND_SPECS`** dans `quiz.models.enums`, alignés sur les slugs API : `nuggets`, `salt_or_pepper`, …). Une seule liaison **OneToOne** non nulle relie ce `Round` à la manche correspondante.

### Champs communs : author, tags, timestamps

#### Author

Tous les modèles de contenu quiz possèdent un champ **`author`** qui référence l'utilisateur ayant créé l'entité :

- **`author`** : ForeignKey vers `CustomUser`, nullable (`SET_NULL` si l'utilisateur est supprimé).
- Automatiquement assigné lors de la création via le JWT de la requête.
- Permet de filtrer le contenu par créateur et de tracer la propriété.

**Modèles concernés** : Question, BurgerQuiz, Nuggets, SaltOrPepper, Menus, MenuTheme, Addition, DeadlyBurger, VideoInterlude.

#### Tags

Tous les modèles de contenu quiz supportent un système de tags via **django-taggit** :

- **`tags`** : TaggableManager permettant d'associer plusieurs tags à une entité.
- Tags normalisés et réutilisables (modèle `Tag` partagé).
- Permet le filtrage, la recherche et le regroupement par tags.

**Usage API** :

```json
{
  "tags": ["humour", "culture-générale"]
}
```

#### Timestamps

Tous les modèles de contenu quiz possèdent des champs d'horodatage :

- **`created_at`** : Date/heure de création (auto, non modifiable).
- **`updated_at`** : Date/heure de dernière modification (auto).

**Modèles concernés** : Question, BurgerQuiz, Nuggets, SaltOrPepper, Menus, MenuTheme, Addition, DeadlyBurger, VideoInterlude.

### Segments « classiques » du jeu (hors modèle)

Ordre éditorial usuel :

- le **Toss**
- les Nuggets, le Sel ou Poivre, les Menus, l’Addition, le Burger de la mort — insérés dans le déroulé via **`BurgerQuizElement`**.

> Le toss est une **manche particulière** côté jeu : petite mission pour départager les équipes et l’équipe qui commence ; seul le **texte** est stocké sur le quiz.

## 2. Question et réponses

### Rôle

Les **Question** décrivent les énoncés ; les **Answer** les propositions (dont une correcte selon les règles de la manche). Le champ **`question_type`** impose la famille (`NU`, `SP`, `ME`, `AD`, `DB`).

### Provenance : `original`

Chaque **Question** possède un booléen **`original`** :
- **`True`** (défaut) : question créée directement (utilisateur / app).
- **`False`** : question issue d'une émission Burger Quiz déjà diffusée.

### Média

- **`video_url`** / **`image_url`** sur la **Question** : optionnels ; hébergement externe, l’app ne stocke que l’URL.
- **`image_url`** sur **Answer** : optionnel (ex. propositions visuelles).

### Réutilisabilité des questions

- **Nuggets** et **Burger de la mort** : une même question (type NU ou DB) peut être **réutilisée** dans plusieurs manches Nuggets / plusieurs DeadlyBurger. Les tables de liaison (**NuggetQuestion**, **DeadlyBurgerQuestion**) n'imposent pas d'unicité sur la question.
- **Sel ou poivre**, **Menu** (**MenuTheme**), **Addition** : les questions sont **propres à une seule** manche / thème / addition. Contrainte d'unicité sur **`question`** dans **SaltOrPepperQuestion**, **MenuThemeQuestion**, **AdditionQuestion**.

### Ordonnancement dans une manche

Des modèles **through** Django relient manche (ou thème) et question avec un champ **`order`** : NuggetQuestion, SaltOrPepperQuestion, MenuThemeQuestion, AdditionQuestion, DeadlyBurgerQuestion.

## 3. Manches

### Provenance : `original` sur les manches

Outre les **Question**, le booléen **`original`** existe sur chaque **manche** (Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger) et sur chaque **MenuTheme**.

### Nuggets

Chaque équipe répond l'une après l'autre à des questions comportant **quatre** propositions et **une** seule bonne réponse. Chaque bonne réponse rapporte 1 miam.

### Sel ou poivre

Réponses rapides en piochant dans une **liste restreinte de propositions** (souvent 2–4 ; max. 5). Ex. « Noir » / « Blanc ».

La manche **SaltOrPepper** expose notamment :

- **`propositions`** (JSON) : liste des choix ; les **Answer** doivent reprendre exactement ces libellés.
- **`description`** (optionnel).

### Les menus

Sur **trois** propositions de thème, chaque équipe répond sur le thème choisi. La manche **Menus** a un **`description`** optionnel ; les thèmes sont des **`MenuTheme`** liés par **`menu_1`**, **`menu_2`**, **`menu_troll`**.

### Addition

Épreuve de rapidité (buzzer) avec contrainte de score (ex. jusqu’aux 25 miams) ; pondération possible selon la partie. **`description`** optionnelle sur **Addition**.

### Burger de la mort

Dix questions dans l’ordre, après écoute des dix questions.


## 4. Interludes vidéo

Un **VideoInterlude** est une vidéo **YouTube** réutilisable dans la structure d’un Burger Quiz (intro, pub, transition, etc.). Le rôle **sémantique** (intro / pub / …) **n’est pas** un champ en base : il repose sur le **titre**, les **tags** et surtout la **position** dans la structure (`BurgerQuizElement.order`).

### Champs

| Champ                | Type            | Description                                                   |
| -------------------- | --------------- | ------------------------------------------------------------- |
| `id`                 | UUID            | Identifiant unique                                            |
| `title`              | string          | Titre de l'interlude (ex: "Intro Burger Quiz", "Pub Ketchup") |
| `youtube_url`        | URL             | URL de la vidéo YouTube                                       |
| `youtube_video_id`   | string          | ID extrait de l'URL YouTube (calculé automatiquement)         |
| `duration_seconds`   | int             | Durée en secondes (optionnel)                                 |
| `autoplay`           | bool            | Lecture automatique (défaut: `true`)                          |
| `skip_allowed`       | bool            | L'utilisateur peut-il passer la vidéo ? (défaut: `true`)      |
| `skip_after_seconds` | int             | Délai avant skip (optionnel, ex: 5)                           |
| `author`             | FK User         | Créateur de l'interlude                                       |
| `tags`               | TaggableManager | Tags associés (ex. `intro`, `pub`)                            |
| `created_at`         | datetime        | Date de création                                              |
| `updated_at`         | datetime        | Date de modification                                          |

### Ordre et présence dans un quiz

Sans ligne **`BurgerQuizElement`** pointant vers un interlude pour un quiz donné, il **n’apparaît pas** dans le déroulé **persisté** de ce quiz. L’ordre est le champ **`order`** des `BurgerQuizElement`.


## 5. Burger Quiz et structure

### Modèle `BurgerQuiz`

Conteneur du jeu : **`title`**, **`toss`**, **`author`**, **`tags`**, **`created_at`** / **`updated_at`**.

L’**ordre des segments** (manches + interludes) est porté uniquement par les **`BurgerQuizElement`** après un **`PUT /api/quiz/burger-quizzes/{id}/structure/`**. Tant qu’aucun enregistrement de structure n’existe, la lecture API du champ **`structure`** est en pratique une **liste vide**.

### Déroulé : `BurgerQuizElement`

Le déroulé est une liste ordonnée de lignes. Chaque ligne a un **`element_type`** logique (**`interlude`** ou **`round`**) et des **FK explicites** vers **`VideoInterlude`** ou **`Round`**.

#### `ELEMENT_TYPES` (vue logique)

| Valeur          | Contenu référencé                 | Modèles en pratique                                                                              |
| --------------- | --------------------------------- | ------------------------------------------------------------------------------------------------ |
| **`interlude`** | Segment **vidéo** dans le déroulé | `VideoInterlude`                                                                                 |
| **`round`**     | **Manche**                        | Instance concrète : `Nuggets`, `SaltOrPepper`, `Menus`, `Addition`, `DeadlyBurger` (via `Round`) |

- **Interlude** : même vidéo **plusieurs fois** possible dans une structure.
- **Round** : chaque **slug** de manche (`nuggets`, `menus`, …) **au plus une fois** par structure ; **`id`** = UUID de la **manche** (= `Round.id` maintenu par les signaux).

L’API utilise des **slugs** (`nuggets`, `salt_or_pepper`, `video_interlude`, …) : sous-type de la ligne quand `element_type` vaut `round` ou pour désigner l’interlude.

#### Champs utiles (rappel)

| Concept        | Rôle                                                   |
| -------------- | ------------------------------------------------------ |
| `burger_quiz`  | Quiz parent                                            |
| `order`        | Rang 1…_n_ dans le déroulé                             |
| `element_type` | `interlude` **ou** `round`                             |
| `interlude`    | FK vers `VideoInterlude` si `element_type = interlude` |
| `round`        | FK vers **`Round`** si `element_type = round`          |

#### Registre `Round`

Une ligne par manche jouable : **`round_type`** (slugs `ROUND_SPECS`) et **exactement une** relation OneToOne vers le modèle concret. **`Round.id`** = UUID de la manche.

### Création du déroulé (résumé)

1. Créer les **manches** et les **VideoInterlude**.
2. Créer le **BurgerQuiz** (sans lier les manches sur ce modèle).
3. **`PUT …/structure/`** avec `elements` : tableau de **`{ "type": "<slug>", "id": "<uuid>" }`** ; la position dans le tableau définit l’ordre.

### Lecture

**`GET …/burger-quizzes/{id}/`** et **`GET …/structure/`** : le **`structure`** reflète les lignes persistées ; **`?expand=full`** sur le détail inclut les objets imbriqués sous la clé du type.

### Exemple de corps `PUT` structure

```json
{
  "elements": [
    { "type": "video_interlude", "id": "uuid-intro" },
    { "type": "nuggets", "id": "uuid-nuggets" },
    { "type": "video_interlude", "id": "uuid-pub" },
    { "type": "addition", "id": "uuid-addition" }
  ]
}
```

Les entrées `video_interlude` correspondent à **`element_type = interlude`** ; les autres slugs de manche à **`round`**.
