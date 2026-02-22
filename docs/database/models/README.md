# Les modèles

## Question : original, média, réutilisabilité

### Original

Chaque **Question** possède un champ booléen **`original`** qui indique sa provenance :

- **`original = True`** (défaut) : question créée directement (par l’utilisateur / l’app).
- **`original = False`** : question issue d’une émission Burger Quiz déjà diffusée.

Chaque manche (Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger) et chaque **thème de menu** (MenuTheme) possède également un champ **`original`**. S’il n’est pas renseigné, il vaut **`true`** (créé directement) ; `false` = issue d’une émission diffusée.

### Média (lien externe)

Une question peut être associée à une **vidéo** et/ou un **image** via des liens externes :

- **`video_url`** : URL vers une vidéo (ex. extrait d’émission).
- **`image_url`** : URL vers un fichier image.

Les deux champs sont optionnels (null/blank). Le contenu est hébergé à l’extérieur ; l’application ne stocke que l’URL.

### Réutilisabilité des questions

- **Nuggets** et **Burger de la mort** : une même question (type NU ou DB) peut être **réutilisée** dans plusieurs manches Nuggets / plusieurs Burger de la mort. Les tables de liaison (NuggetQuestion, DeadlyBurgerQuestion) n’imposent pas d’unicité sur la question.
- **Sel ou poivre**, **Menu** (MenuTheme), **Addition** : les questions sont **propres à une seule manche**. Une question de type SP, ME ou AD n’appartient qu’à un seul Sel ou poivre, un seul thème de menu, ou une seule Addition. C’est assuré en base par une contrainte d’unicité sur `question` dans SaltOrPepperQuestion, MenuThemeQuestion et AdditionQuestion.

---

## Burger Quiz

Un burger quiz est un ensemble de manches, chaque manche comprenant une suite de questions. Le modèle **BurgerQuiz** comporte **`created_at`** et **`updated_at`** (horodatage de création et de dernière modification) pour l’affichage liste (date/création) et le tri. Les manches sont dans l’ordre :
- le Toss*
- les Nuggets
- le Sel ou Poivre
- les Menus
- l'addition
- le burger de la mort

On utilise les modèles Question/Answer pour décrire les questions et réponses de toutes les manches.

Des modèles intermédiaires (NuggetQuestion, SaltOrPepperQuestion, MenuThemeQuestion, AdditionQuestion, DeadlyBurgerQuestion) permettent d’ordonner les questions au sein de chaque manche via un champ `order`.

> * Le toss est une manche particulière, consistant en une petite mission pour départager le choix des équipes et l'équipe qui débute.

## Nuggets

Chaque équipe répond l'une après l'autre à des questions comportant quatre propositions et une seule solution. Chaque bonne réponse rapporte 1 miam.

## Sel ou poivre

Les candidats doivent répondre le plus vite possible à une série de questions en piochant parmi une **liste restreinte de propositions** donnée en début de manche (souvent 2, 3 ou 4 ; maximum 5). Exemples : « Noir » / « Blanc », ou « Noir » / « Blanc » / « Les deux ».

La manche **SaltOrPepper** possède un champ **`choice_labels`** (liste de chaînes) qui définit ces propositions. Chaque question de la manche doit avoir des réponses (Answer) dont le libellé est exactement l’un de ces choix.

## Les menus

Sur une liste de trois propositions de thème, chaque équipe doit répondre à une série de questions sur le thème choisi.

## Addition

Épreuve de rapidité lors de laquelle les équipes doivent buzzer pour répondre à un questionnaire comportant une contrainte jusqu'à atteindre les 25 miams. Selon l'avancement des scores, les questions peuvent valoir davantage de points

## Burger de la mort

Un membre de l'équipe gagnante doit répondre à 10 questions dans l'ordre seulement après avoir écouté les 10 questions.


## 2. Champ `original` (questions et manches)

La **provenance** (contenu issue d’une émission diffusée ou créé manuellement) est portée par un booléen **`original`** à la fois sur les **Question** et sur les **manches** (Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger).

### 2.1 En base de données

- Chaque **Question** possède un champ **`original`** (booléen, défaut **`true`**). **`original = True`** = créée directement, **`original = False`** = issue d’une émission diffusée.
- Chaque **manche** (Nuggets, SaltOrPepper, Menus, Addition, DeadlyBurger) et chaque **MenuTheme** possède un champ **`original`** (booléen). S’il n’est pas renseigné, valeur par défaut **`true`** (créé directement).

### 2.2 Règles API

- **Création / mise à jour d’une Question** : le champ **`question_type`** est obligatoire ; le champ **`original`** est optionnel (défaut **`true`** = créée directement).
- **GET liste/détail des questions** : filtrage par **`?original=true|false`** et par **`?question_type=NU|SP|ME|AD|DB`**.
- **Manches et thèmes de menu** : le champ **`original`** est accepté en création et mise à jour (POST/PATCH), optionnel (défaut **`true`**). Il est renvoyé en GET (liste et détail).

### 2.4 Réutilisabilité des questions

- **Nuggets** et **Burger de la mort** : une même question (type NU ou DB) peut être **réutilisée** dans plusieurs manches. On peut donc référencer une question déjà utilisée dans un autre Nuggets / un autre Burger de la mort.
- **Sel ou poivre**, **Menu** (MenuTheme), **Addition** : les questions sont **propres à une seule manche**. Une question de type SP, ME ou AD ne peut appartenir qu’à un seul Sel ou poivre, un seul thème de menu, ou une seule Addition. En base, une contrainte d’unicité l’impose ; l’API doit refuser d’ajouter une question déjà liée à une autre manche du même type.

### 2.5 Média (lien externe sur une question)

Une question peut être associée à une **vidéo** et/ou un **image** via des liens externes :

- **`video_url`** : URL optionnelle vers une vidéo (ex. extrait d’émission).
- **`image_url`** : URL optionnelle vers un fichier image.

Les deux champs sont optionnels. L’endpoint de création/mise à jour de questions doit les accepter et les valider (format URL).