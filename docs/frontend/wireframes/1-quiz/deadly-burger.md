# Wireframes — Burger de la mort

Réf. : [page_reference](../../page_reference.md) · [README](README.md) · [components](../../components.md)

## Sommaire

- [DeadlyBurgerListPage](#1-deadlyburgerlistpage)
- [DeadlyBurgerDetailPage](#2-deadlyburgerdetailpage)
- [DeadlyBurgerCreatePage / DeadlyBurgerEditPage](#3-deadlyburgercreatepage--deadlyburgereditpage)
- [DeadlyBurgerForm (modale depuis BurgerQuizDetailEdit)](#4-deadlyburgerform-modale)
- [DeadlyBurgerQuestionInlineForm](#5-deadlyburgerquestioninlineform)

---

## 1 - DeadlyBurgerListPage

### Principe

Tableau des manches Burger de la mort : colonnes titre, original ?, nombre d'utilisation, nombre de questions. Bouton Ajouter → DeadlyBurgerCreatePage.  
**Actions** : détail, édition, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manches Burger de la mort                    [ + Ajouter ]      |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre Q | Actions  |
|------------------|------------|--------------|--------|-----------|
|  Finale épique   | oui        | 2            | 10     | [👁][✏️][🗑] |
|  Challenge ultime| non        | 1            | 10     | [👁][✏️][🗑] |
|  ...             | ...        | ...          | ...    | ...      |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/deadly-burgers/` | [api-reference](../../../backend/api-reference.md) §2.6 |

---

## 2 - DeadlyBurgerDetailPage

### Principe

Affichage : titre, original, liste des 10 questions dans l'ordre (énoncé uniquement, type DB = pas de réponses à afficher). Actions : DeadlyBurgerEditPage, suppression (modale).

### Wireframe

```
+------------------------------------------------------------------+
|  Manche Burger de la mort — Finale épique                         |
+------------------------------------------------------------------+
|  Titre    : Finale épique                                         |
|  Original : oui                                                   |
|                                                                   |
|  Questions (10) :                                                 |
|  ┌────────────────────────────────────────────────────────────┐  |
|  | 1. Quel est le plus grand océan du monde ?                  |  |
|  | 2. En quelle année a été construite la Tour Eiffel ?        |  |
|  | 3. Qui a peint la Joconde ?                                 |  |
|  | 4. ...                                                      |  |
|  | 10. Quelle est la capitale du Japon ?                       |  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [Modifier]                                    [Supprimer]        |
+------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                         | Réf.                                                    |
| ------ | ------- | -------------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/deadly-burgers/{id}/` | [api-reference](../../../backend/api-reference.md) §2.6 |

---

## 3 - DeadlyBurgerCreatePage / DeadlyBurgerEditPage

### Principe

Page dédiée pour créer/modifier une manche Burger de la mort. **Exactement 10 questions** requises (type DB). Les questions n'ont pas de réponses à saisir (oral). Possibilité de piocher dans les questions existantes via modale de recherche.

### Wireframe

```
+------------------------------------------------------------------+
|  Créer une manche Burger de la mort  (ou Modifier)                |
+------------------------------------------------------------------+
|                                                                   |
|  <DeadlyBurgerForm />                                             |
|                                                                   |
|  Titre *   [________________________________________________]     |
|  Original  [ ] Cette manche est originale                         |
|                                                                   |
|  Questions (exactement 10, type DB)                               |
|  ┌────────────────────────────────────────────────────────────┐  |
|  │ <DeadlyBurgerQuestionInlineForm />                          │  |
|  │ 1  | [___________________________________________]  [🗑]    │  |
|  │    | [✓ Sauvegardée]                            [Valider]   │  |
|  ├────────────────────────────────────────────────────────────┤  |
|  │ 2  | [___________________________________________]  [🗑]    │  |
|  │    | [⏳ Non sauvée]                            [Valider]   │  |
|  ├────────────────────────────────────────────────────────────┤  |
|  │ ...                                                         │  |
|  ├────────────────────────────────────────────────────────────┤  |
|  │ 10 | [___________________________________________]  [🗑]    │  |
|  │    | [📝 Nouvelle]                              [Valider]   │  |
|  └────────────────────────────────────────────────────────────┘  |
|                                                                   |
|  [+ Ajouter une question]  (si < 10)                              |
|  [Remplir avec des questions existantes]  (ouvre modale recherche)|
|                                                                   |
|  [Annuler]                                      [Enregistrer]     |
+------------------------------------------------------------------+
```

### Appels API

| Action                                | Méthode   | Endpoint                                           | Réf.                                                    |
| ------------------------------------- | --------- | -------------------------------------------------- | ------------------------------------------------------- |
| Créer                                 | POST      | `/api/quiz/deadly-burgers/`                        | [api-reference](../../../backend/api-reference.md) §2.6 |
| Modifier                              | PUT/PATCH | `/api/quiz/deadly-burgers/{id}/`                   | idem                                                    |
| Questions (liste / recherche type DB) | GET       | `/api/quiz/questions/?question_type=DB&search=...` | §2.1                                                    |

---

## 4 - DeadlyBurgerForm (modale)

### Principe

Formulaire utilisé dans une modale depuis `BurgerQuizDetailEdit` pour créer ou éditer une manche Burger de la mort directement attachée au quiz.

### Wireframe (dans modale)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Créer une manche Burger de la mort                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  <DeadlyBurgerForm />                                               │
│                                                                     │
│  Titre *   [________________________________________________]       │
│  Original  [ ] Cette manche est originale                           │
│                                                                     │
│  Questions (exactement 10)                                          │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ <DeadlyBurgerQuestionInlineForm />                         │     │
│  │ 1  | [_________________________________________]  [🗑]      │     │
│  │    | [✓ Sauvegardée]                          [Valider]    │     │
│  ├────────────────────────────────────────────────────────────┤     │
│  │ 2  | [_________________________________________]  [🗑]      │     │
│  │    | [⏳ Non sauvée]                          [Valider]    │     │
│  ├────────────────────────────────────────────────────────────┤     │
│  │ ...                                                        │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                     │
│  [+ Ajouter une question]  (si < 10)                                │
│  [Remplir avec des questions existantes]                            │
│                                                                     │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Enregistrer]    │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux

```
<DeadlyBurgerModal /> (depuis BurgerQuizDetailEdit)
     │
     ▼
<DeadlyBurgerForm />
     │
     ├── Saisie titre, original
     │
     ├── Ajout de questions (jusqu'à 10)
     │     │
     │     ├── Option 1: Création manuelle
     │     │     └── <DeadlyBurgerQuestionInlineForm />
     │     │           ├── Saisie énoncé (pas de réponse)
     │     │           ├── [Valider] → sauvegarde locale
     │     │           └── Statut affiché (✓ | ⏳ | ⚠️)
     │     │
     │     └── Option 2: Questions existantes
     │           │
     │           ▼
     │         <SearchAndSelectDeadlyBurgerQuestions />
     │           ├── Recherche questions type DB
     │           ├── Sélection multiple
     │           └── Ajout à la liste
     │
     ▼
{Validation: exactement 10 questions}
     │
     ▼
(Clic "Enregistrer")
     │
     ▼
[[POST /api/quiz/deadly-burgers/]]
     │
     ├── ✅ 201 Created
     │        │
     │        ▼
     │   [[PATCH /api/burger-quiz/:id/]] { deadly_burger_id: newId }
     │        │
     │        ▼
     │   Fermer modale + toast "Manche créée"
     │
     └── ❌ 400 Bad Request
              │
              ▼
         Afficher erreurs dans le formulaire
         (ex: "10 questions requises, vous en avez 7")
```

---

## 5 - DeadlyBurgerQuestionInlineForm

### Principe

Composant inline pour saisir une question Burger de la mort. **Énoncé seul** (pas de réponse à saisir car la manche est orale). Inclut un bouton **Valider** et un **statut de sauvegarde**.

### Props

```typescript
interface DeadlyBurgerQuestionInlineFormProps {
  question?: DeadlyBurgerQuestion; // Question existante (édition)
  index: number; // Position (1-10)
  onSave: (data: DeadlyBurgerQuestionData) => void;
  onRemove?: () => void;
  isFromSearch?: boolean; // Question importée (lecture seule)
}
```

### États de sauvegarde

| Statut     | Icône | Description                   | Couleur |
| ---------- | ----- | ----------------------------- | ------- |
| `new`      | 📝    | Nouvelle question             | Gris    |
| `dirty`    | ⏳    | Non sauvegardée               | Jaune   |
| `saving`   | ⏳    | Sauvegarde en cours           | Bleu    |
| `saved`    | ✓     | Sauvegardée                   | Vert    |
| `error`    | ⚠️    | Erreur de validation/save     | Rouge   |
| `imported` | 🔗    | Importée (question existante) | Bleu    |

### Wireframe détaillé

```
┌─────────────────────────────────────────────────────────────────┐
│  Question 1                                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Énoncé *  [________________________________________________]   │
│                                                                 │
│  (Pas de réponse à saisir — manche orale)                       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Statut : ✓ Sauvegardée                                      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  [Valider]                                              [🗑]     │
└─────────────────────────────────────────────────────────────────┘
```

### Wireframe compact (dans liste)

```
┌──────────────────────────────────────────────────────────────────┐
│ 1  | [___________________________________________]  [🗑]          │
│    | [✓ Sauvegardée]                            [Valider]        │
└──────────────────────────────────────────────────────────────────┘
```

### Wireframe question importée (lecture seule)

```
┌──────────────────────────────────────────────────────────────────┐
│ 3  | Quel est le plus grand océan du monde ?        [👁] [🗑]     │
│    | [🔗 Question existante #42]                                 │
└──────────────────────────────────────────────────────────────────┘
```

### Flux de validation

```
<DeadlyBurgerQuestionInlineForm />
     │
     ├── Statut initial: 📝 Nouvelle
     │
     ▼
(Saisie énoncé)
     │
     ├── Statut: ⏳ Non sauvegardée (dirty)
     │
     ▼
(Clic "Valider")
     │
     ▼
{Validation locale}
     │
     ├── ❌ Erreur
     │        │
     │        ▼
     │   Statut: ⚠️ Erreur + messages inline
     │   • "L'énoncé est requis"
     │   • "L'énoncé doit faire au moins 10 caractères"
     │
     └── ✅ Valide
              │
              ▼
         Statut: ✓ Sauvegardée (vert)
         Données stockées localement
         (envoi API au submit du formulaire parent)
```

### Validation

| Champ  | Règle                     |
| ------ | ------------------------- |
| Énoncé | Requis, min 10 caractères |

### Contrainte formulaire parent

```
{Avant soumission du DeadlyBurgerForm}
     │
     ▼
{Validation globale}
     │
     ├── Nombre de questions ≠ 10
     │        │
     │        ▼
     │   Erreur: "Exactement 10 questions requises (actuellement: X)"
     │   Bouton "Enregistrer" désactivé
     │
     └── Nombre de questions = 10 + toutes validées
              │
              ▼
         Soumission autorisée
```

---

## 6 - Modale recherche questions existantes

### Principe

Permet de sélectionner des questions existantes (type DB) pour les ajouter à la manche. Les questions déjà présentes dans la manche sont grisées.

### Wireframe

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Ajouter des questions existantes                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Recherche : [_______________________] 🔍                            │
│                                                                      │
│  Questions disponibles (type DB) :                                   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ☐ Quel est le plus grand océan du monde ?                    │   │
│  │ ☐ En quelle année a été construite la Tour Eiffel ?          │   │
│  │ ☑ Qui a peint la Joconde ?  ← sélectionnée                   │   │
│  │ ░░ Quelle est la capitale du Japon ? ░░  ← déjà dans la manche│   │
│  │ ☑ Combien de planètes dans le système solaire ?              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Sélectionnées : 2 / Places restantes : 3                           │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                         [Ajouter (2)]     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Appels API récapitulatifs

| Action                         | Méthode | Endpoint                                           | Réf. |
| ------------------------------ | ------- | -------------------------------------------------- | ---- |
| Lister manches                 | GET     | `/api/quiz/deadly-burgers/`                        | §2.6 |
| Détail manche                  | GET     | `/api/quiz/deadly-burgers/{id}/`                   | §2.6 |
| Créer manche                   | POST    | `/api/quiz/deadly-burgers/`                        | §2.6 |
| Modifier manche                | PATCH   | `/api/quiz/deadly-burgers/{id}/`                   | §2.6 |
| Supprimer manche               | DELETE  | `/api/quiz/deadly-burgers/{id}/`                   | §2.6 |
| Rechercher questions (type DB) | GET     | `/api/quiz/questions/?question_type=DB&search=...` | §2.1 |
