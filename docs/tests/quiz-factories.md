# Factories du module Quiz

Ce document décrit les **factories** utilisées pour créer les données de test du module `quiz`. Implémentation : **`backend/src/quiz/tests/factories.py`**.

## Technologie

Les données de test sont créées via **factory_boy** (dépendance du groupe `dev`). Les factories utilisent :

- **`DjangoModelFactory`** pour les modèles Django ;
- **`SubFactory`** pour les clés étrangères (ex. `MenusFactory` → `MenuThemeFactory`) ;
- **`@factory.post_generation`** pour les relations M2M avec table through (Nuggets, MenuTheme, Addition, DeadlyBurger, SaltOrPepper).

**Installation** : `uv sync --group dev` depuis `backend/`.

---

## QuestionFactory

- **`QuestionFactory.create_nu(text=..., original=...)`** — Question type Nuggets
- **`QuestionFactory.create_sp(...)`** — Question type Sel ou poivre
- **`QuestionFactory.create_me(...)`** — Question type Menu
- **`QuestionFactory.create_ad(...)`** — Question type Addition
- **`QuestionFactory.create_db(...)`** — Question type Burger de la mort
- **`QuestionFactory.create_nu_with_answers(text=..., correct_index=2)`** — Question NU avec 4 réponses (une correcte)

---

## NuggetsFactory

- **`NuggetsFactory.create(title=..., original=..., questions=[q1, q2, ...])`** — Manche Nuggets, optionnellement avec questions (ordre préservé)

---

## SaltOrPepperFactory

- **`SaltOrPepperFactory.create(title=..., choice_labels=[...], original=..., description=...)`** — Manche Sel ou poivre

---

## MenuThemeFactory

- **`MenuThemeFactory.create_classic(title=..., question_ids=...)`** — Thème type CL
- **`MenuThemeFactory.create_troll(title=..., question_ids=...)`** — Thème type TR

---

## MenusFactory

- **`MenusFactory.create(title=..., menu_1=..., menu_2=..., menu_troll=..., original=...)`** — Manche Menus (si menu_1/menu_2/menu_troll non fournis, des thèmes par défaut sont créés)

---

## AdditionFactory

- **`AdditionFactory.create(title=..., original=..., questions=[...])`** — Manche Addition

---

## DeadlyBurgerFactory

- **`DeadlyBurgerFactory.create(title=..., original=..., questions=[...])`** — Manche Burger de la mort
- **`DeadlyBurgerFactory.create_with_ten_questions(title=...)`** — Manche DB avec 10 questions créées automatiquement

---

## BurgerQuizFactory

- **`BurgerQuizFactory.create(title=..., toss=..., nuggets=..., salt_or_pepper=..., menus=..., addition=..., deadly_burger=...)`** — Burger Quiz (tous les IDs de manches optionnels)
- **`BurgerQuizFactory.create_full(title=..., toss=...)`** — Burger Quiz avec toutes les manches (Nuggets, SOP, Menus, Addition, DB) créées automatiquement

---

## Exemple d’usage dans un test

```python
from ...tests.factories import QuestionFactory, NuggetsFactory

q1 = QuestionFactory.create_nu("N1")
q2 = QuestionFactory.create_nu("N2")
nuggets = NuggetsFactory.create(title="Culture générale", questions=[q1, q2])
```
