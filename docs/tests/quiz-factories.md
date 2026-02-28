# Factories du module Quiz

Ce document décrit les **factories** utilisées pour créer les données de test du module `quiz`. Implémentation : **`backend/src/quiz/tests/factories.py`**.

## Technologie

Les données de test sont créées via **factory_boy** (dépendance du groupe `dev`). Les factories utilisent :

- **`DjangoModelFactory`** pour les modèles Django ;
- **`SubFactory`** pour les clés étrangères (ex. `MenusFactory` → `MenuThemeFactory`) ;
- **`@factory.post_generation`** pour les relations M2M avec table through (Nuggets, MenuTheme, Addition, DeadlyBurger, SaltOrPepper) et pour les tags.

**Installation** : `uv sync --group dev` depuis `backend/`.

---

## UserFactory

Factory pour créer des utilisateurs de test (auteurs de contenu).

- **`UserFactory.create(username=..., email=...)`** — Utilisateur de test
- **`UserFactory.create_author(username="author")`** — Utilisateur destiné à être auteur de contenu

---

## QuestionFactory

Toutes les méthodes supportent les paramètres optionnels `author` et `tags`.

### Création unitaire

- **`QuestionFactory.create_nu(text=..., original=..., author=..., tags=[...])`** — Question type Nuggets
- **`QuestionFactory.create_sp(...)`** — Question type Sel ou poivre
- **`QuestionFactory.create_me(...)`** — Question type Menu
- **`QuestionFactory.create_ad(...)`** — Question type Addition
- **`QuestionFactory.create_db(...)`** — Question type Burger de la mort

### Création avec réponses

- **`QuestionFactory.create_nu_with_answers(text=..., correct_index=2, author=..., tags=[...])`** — Question NU avec 4 réponses (une correcte)
- **`QuestionFactory.create_sp_with_answers(text=..., propositions=[...], correct_index=0, author=..., tags=[...])`** — Question SP avec réponses basées sur les propositions
- **`QuestionFactory.create_ad_with_answer(text=..., answer_text="42", author=..., tags=[...])`** — Question AD avec une réponse

### Création par batch

- **`QuestionFactory.create_batch_nu(count, author=..., tags=[...])`** — Batch de questions Nuggets avec réponses
- **`QuestionFactory.create_batch_sp(count, propositions=[...], author=..., tags=[...])`** — Batch de questions Sel ou Poivre avec réponses
- **`QuestionFactory.create_batch_ad(count, author=..., tags=[...])`** — Batch de questions Addition avec réponses
- **`QuestionFactory.create_batch_db(count, author=..., tags=[...])`** — Batch de questions Burger de la mort (sans réponses)

---

## NuggetsFactory

- **`NuggetsFactory.create(title=..., original=..., author=..., tags=[...], questions=[q1, q2, ...])`** — Manche Nuggets, optionnellement avec questions (ordre préservé)
- **`NuggetsFactory.create_with_questions(title=..., questions=[...], author=..., tags=[...])`** — Manche Nuggets avec questions (crée 4 questions par défaut si non fournies)

---

## SaltOrPepperFactory

- **`SaltOrPepperFactory.create(title=..., choice_labels=[...], original=..., description=..., author=..., tags=[...])`** — Manche Sel ou poivre
- **`SaltOrPepperFactory.create(propositions=[...])`** — Alias pour `choice_labels` (plus lisible)
- **`SaltOrPepperFactory.create_with_questions(title=..., propositions=[...], questions=[...], author=..., tags=[...])`** — Manche SP avec questions (crée 3 questions par défaut si non fournies)

---

## MenuThemeFactory

- **`MenuThemeFactory.create_classic(title=..., question_ids=..., author=..., tags=[...])`** — Thème type CL
- **`MenuThemeFactory.create_troll(title=..., question_ids=..., author=..., tags=[...])`** — Thème type TR

---

## MenusFactory

- **`MenusFactory.create(title=..., menu_1=..., menu_2=..., menu_troll=..., original=..., author=..., tags=[...])`** — Manche Menus (si menu_1/menu_2/menu_troll non fournis, des thèmes par défaut sont créés)

---

## AdditionFactory

- **`AdditionFactory.create(title=..., original=..., author=..., tags=[...], questions=[...])`** — Manche Addition
- **`AdditionFactory.create_with_questions(title=..., questions=[...], author=..., tags=[...])`** — Manche Addition avec questions (crée 3 questions par défaut si non fournies)

---

## DeadlyBurgerFactory

- **`DeadlyBurgerFactory.create(title=..., original=..., author=..., tags=[...], questions=[...])`** — Manche Burger de la mort
- **`DeadlyBurgerFactory.create_with_ten_questions(title=..., author=..., tags=[...])`** — Manche DB avec 10 questions créées automatiquement

---

## VideoInterludeFactory

Factory pour créer des interludes vidéo.

- **`VideoInterludeFactory.create(title=..., youtube_url=..., interlude_type=..., author=..., tags=[...])`** — Interlude générique
- **`VideoInterludeFactory.create_intro(title="Intro", author=..., tags=[...])`** — Interlude de type Intro (`IN`)
- **`VideoInterludeFactory.create_outro(title="Outro", author=..., tags=[...])`** — Interlude de type Outro (`OU`)
- **`VideoInterludeFactory.create_pub(title="Pub", author=..., tags=[...])`** — Interlude de type Pub (`PU`)

**Paramètres optionnels** : `duration_seconds`, `autoplay`, `skip_allowed`, `skip_after_seconds`.

---

## BurgerQuizFactory

- **`BurgerQuizFactory.create(title=..., toss=..., author=..., tags=[...], nuggets=..., salt_or_pepper=..., menus=..., addition=..., deadly_burger=...)`** — Burger Quiz (tous les IDs de manches optionnels)
- **`BurgerQuizFactory.create_full(title=..., toss=..., author=..., tags=[...])`** — Burger Quiz avec toutes les manches (Nuggets, SOP, Menus, Addition, DB) créées automatiquement
- **`BurgerQuizFactory.create_with_structure(title=..., toss=..., interludes={...}, author=..., tags=[...])`** — Burger Quiz complet avec structure personnalisée

**Paramètre `interludes`** pour `create_with_structure` :

```python
{
    "intro": intro_interlude,       # VideoInterlude pour l'intro
    "outro": outro_interlude,       # VideoInterlude pour l'outro
    "pubs": [                       # Liste d'interludes pub avec position
        {"after": "NU", "interlude": pub1},
        {"after": "ME", "interlude": pub2},
    ]
}
```

---

## BurgerQuizElementFactory

Factory pour créer des éléments de structure (manches ou interludes ordonnés).

- **`BurgerQuizElementFactory.create_round(burger_quiz, order, round_type)`** — Élément de type manche
- **`BurgerQuizElementFactory.create_interlude(burger_quiz, order, interlude)`** — Élément de type interlude

**Exemple** :

```python
from ..factories import BurgerQuizFactory, VideoInterludeFactory, BurgerQuizElementFactory

bq = BurgerQuizFactory.create_full()
intro = VideoInterludeFactory.create_intro()

BurgerQuizElementFactory.create_interlude(bq, order=1, interlude=intro)
BurgerQuizElementFactory.create_round(bq, order=2, round_type="NU")
BurgerQuizElementFactory.create_round(bq, order=3, round_type="SP")
```

---

## Exemple d'usage dans un test

```python
from ...tests.factories import QuestionFactory, NuggetsFactory, UserFactory

# Créer un auteur
author = UserFactory.create_author(username="quiz_creator")

# Créer des questions avec auteur et tags
q1 = QuestionFactory.create_nu("N1", author=author, tags=["culture", "facile"])
q2 = QuestionFactory.create_nu("N2", author=author, tags=["sport"])

# Créer une manche Nuggets avec auteur et tags
nuggets = NuggetsFactory.create(
    title="Culture générale",
    author=author,
    tags=["quiz", "original"],
    questions=[q1, q2]
)
```

## Paramètres communs

Toutes les factories supportent les paramètres suivants :

| Paramètre | Type | Description |
|-----------|------|-------------|
| `author` | `User` ou `None` | Utilisateur auteur du contenu (optionnel) |
| `tags` | `list[str]` ou `None` | Liste de tags à associer (optionnel) |

Ces paramètres sont gérés via `@factory.post_generation` pour les tags et directement comme attribut pour l'author (FK).
